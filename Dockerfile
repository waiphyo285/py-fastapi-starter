# Use official Python image
FROM python:3.11-slim-buster

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . .

# Expose port
EXPOSE 9001

# Run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9001"]
