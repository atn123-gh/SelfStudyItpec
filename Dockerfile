# Pull base image
FROM python:3.11.4-slim-bullseye

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /code

# Copy project
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements/production.txt

# Make entrypoint script executable
RUN chmod +x entrypoint.sh && ls -l entrypoint.sh


