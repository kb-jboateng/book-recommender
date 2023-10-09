# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /code

# Add application code to the container
COPY ./app /code/app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt /code/

# Copy the env file into the container at /app
COPY .env /code/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

CMD ["uvicorn", "app.main:app"]