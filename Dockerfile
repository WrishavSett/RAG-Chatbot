# Use the official Python image as a base
FROM python:3.11-slim

# Set working directory in the container
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port 3000 to the outside world
EXPOSE 8501

# Run the Flask app
CMD ["streamlit", "run", "app.py","--server.address=0.0.0.0"]
