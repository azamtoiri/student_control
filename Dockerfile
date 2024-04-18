# Use an official Python runtime as a parent image
FROM python:3.11-alpine

# Set the working directory in the container to /app
WORKDIR /app

# Copy only requirements to cache them in docker layer
ADD requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN #pip install poetry

# Copying the rest of the code
COPY . /app

RUN #poetry install --no-root

RUN pip install -r requirements.txt

RUN #alembic upgrade head
# Run migrations (assuming there's a script for it)

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]