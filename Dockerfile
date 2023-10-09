# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt /app/

# Copy the env file into the container at /app
COPY .env /app/

# Add your application code to the container
COPY ./app /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

CMD ["uvicorn", "app.main:app"]