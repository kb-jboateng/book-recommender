#!/bin/sh
./stop_docker.sh
docker build -t recommender .
docker run -d --name book_recommender -p 80:80 recommender
docker logs -f book_recommender
