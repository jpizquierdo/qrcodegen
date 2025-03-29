# Use the official Python slim image
FROM python:3.12-slim

# Set environment variables
#PYTHONUNBUFFERED=1: Ensures Python output is not buffered, making logs immediately visible.
#PYTHONDONTWRITEBYTECODE=1: Prevents Python from writing .pyc files, reducing unnecessary writes.
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set the working directory
WORKDIR /code

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY app app

# Create a non-root user for security
RUN useradd -m appuser

# Grant ownership of the /app directory to the appuser
RUN chown -R appuser:appuser /code

# Switch to the non-root user
USER appuser

# Run the application
CMD ["python", "app/app.py"]