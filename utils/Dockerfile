# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file into the container
COPY ./requirements.txt /code/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy all project files into the container
COPY . .

# Grant permissions to write files inside uploads/ and reports/
RUN mkdir -p uploads reports && chmod -R 777 uploads reports

# Expose port 7860 (Hugging Face Spaces expects this port)
EXPOSE 7860

# Start FastAPI using Uvicorn bound to port 7860
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
