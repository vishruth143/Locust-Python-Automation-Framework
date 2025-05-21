# Use official Python image as base
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

# Expose the port Locust runs on (default 8089)
EXPOSE 8089

# Default command to run Locust in headless mode with your params
CMD ["locust", "-f", "locustfile.py", "--headless", "-u", "10", "-r", "2", "-t", "1m", "--html=reports/report.html"]
