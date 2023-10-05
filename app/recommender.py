import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix
from sklearn.metrics.pairwise import cosine_similarity

from database import engine

def recommend_books(user_id: str):
    try:
        books = __get_books()
        similar_users = __get_similar_users(user_id, books)
        if len(similar_users) > 0:
            recommend_books = __get_recommended_books(similar_users, books)
            return recommend_books
        else:
            return []
    except Exception as e:
        return []

def __get_books():
    query = "SELECT * FROM recommender_view"
    books = pd.read_sql_query(query, con=engine)
    books['book_id'] = pd.to_numeric(books['book_id'])
    books['user_index'] = pd.to_numeric(books['user_index'])
    books['book_index'] = pd.to_numeric(books['book_index'])
    books['number_of_ratings'] = pd.to_numeric(books['number_of_ratings'])
    books['rating'] = pd.to_numeric(books['book_id'])
    books['user_id'] = books['user_id'].astype(str)

    return books

def __get_similar_users(user_id: str, books):
    user_index = books[books['user_id'] == user_id]['user_index'].iloc[0]
    books_liked_by_user = set(books[books['user_id'] == user_id]['book_id'])
    count_other_similar_users = books[books['book_id'].isin(books_liked_by_user)]['user_id'].value_counts()
    similar_users = count_other_similar_users.to_frame().reset_index()
    similar_users.columns = ['user_id', 'matching_book_count']
    top_onepercent_similar_users = similar_users[similar_users['matching_book_count']>=np.percentile(similar_users['matching_book_count'], 99)]
    top_users = set(top_onepercent_similar_users['user_id'])
    similar_users = books[(books['user_id'].isin(top_users))]
    ratings_mat_coo = coo_matrix((similar_users["rating"], (similar_users["user_index"], similar_users["book_index"])))
    ratings_mat = ratings_mat_coo.tocsr()
    similarity = cosine_similarity(ratings_mat[user_index, :], ratings_mat).flatten()
    similar_users_index = np.argsort(similarity)[-2:-52:-1]
    similar_users_refined = similar_users[((similar_users["user_index"].isin(similar_users_index)) & (~similar_users['book_id'].isin(books_liked_by_user)))].copy()
    return similar_users_refined

def __get_recommended_books(similar_users, books):
    all_records = similar_users['book_id'].value_counts()
    all_records = all_records.to_frame().reset_index()
    all_records.columns = ['book_id', 'book_count']
    all_records_book_ids = list(all_records['book_id'].unique())
    new_records = books[books['book_id'].isin(all_records_book_ids)]
    stats = new_records.groupby("book_id").rating.agg(["count", "mean"])
    new_records = new_records.merge(all_records, on='book_id', how='inner')
    new_records = new_records.merge(stats, on='book_id', how='inner')
    new_records['adjusted_count'] = (new_records['book_count'] * (new_records['book_count'] / new_records['number_of_ratings'])) / 100
    new_records["score"] = new_records["mean"] * new_records["adjusted_count"] * 100
    records_by_score = new_records.sort_values(by='score', ascending=False)
    return records_by_score.iloc[:15]['book_id'].tolist() if len(records_by_score) > 0 else []