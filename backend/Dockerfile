# Use an official Python runtime as the base image
FROM docker.arvancloud.ir/python:3.11-slim

# Set environment variables to prevent Python from writing .pyc files
# and to set up the Django settings module for production
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt --no-deps

# Copy the Django project code
COPY . /app/

# Copy the .env file for environment variables (optional, adjust as needed)
COPY .env /app/

EXPOSE 8000
# Run migrations and then start the development server
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
