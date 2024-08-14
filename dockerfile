
FROM python

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Excel-related dependencies (if any)
# Uncomment the following line if your application requires specific system dependencies for Excel handling
# RUN apt-get install -y libxml2 libxslt1-dev zlib1g-dev

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . /app/

# Specify the command to run on container start
# If your script needs command-line arguments, adjust accordingly
CMD ["python", "attempt3.py"]
