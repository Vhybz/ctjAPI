# Use official Python 3.11 image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy all code
COPY . .

# Expose port
EXPOSE 10000

# Start API
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "my_api:app", "--bind", "0.0.0.0:10000"]
