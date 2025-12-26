# Use official Python base image
FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Set environment variables if needed
ENV PYTHONUNBUFFERED=1

# Command to run your app
CMD ["python", "-m", "backend.ui.chat_ui"]
