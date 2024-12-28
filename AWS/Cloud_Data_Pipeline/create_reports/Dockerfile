FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
    curl \
    gnupg2 \
    wget && \
    rm -rf /var/lib/apt/lists/*

# Configure Microsoft repository
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list

# Force remove conflicting packages and install ODBC
RUN apt-get update && \
    apt-get remove -y unixodbc unixodbc-dev && \
    apt-get install --no-install-recommends -y \
    unixodbc \
    unixodbc-dev && \
    ACCEPT_EULA=Y DEBIAN_FRONTEND=noninteractive apt-get install -y msodbcsql18 && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./queries/ ./queries/
COPY main.py .

# Run the script
CMD ["python", "main.py"]