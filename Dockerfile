# Use an official Python runtime as the base image
FROM python:3.10

# Install system dependencies for ODBC and SQL Server
RUN apt-get update && apt-get install -y \
    unixodbc-dev \
    gcc \
    libpq-dev \
    libssl-dev \
    libsasl2-dev \
    libldap2-dev \
    libffi-dev \
    curl && \
    curl -sSL https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl -sSL https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17 && \
    apt-get clean


# Set the working directory in the container
WORKDIR /app

# Copy all necessary files with exact names
COPY App.py /app/App.py
COPY Authentication.py /app/Authentication.py
COPY Models.py /app/Models.py
COPY requirements.txt /app/requirements.txt
COPY Swagger.yml /app/Swagger.yml

# Copy the "api" directory
COPY api /app/api

# Copy the "templates" directory
COPY templates /app/templates

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Expose the application port
EXPOSE 5000

# Set environment variables for Flask 
ENV FLASK_APP=App.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the application
CMD ["python", "/app/App.py"]
