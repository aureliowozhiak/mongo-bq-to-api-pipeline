FROM apache/airflow:2.8.1-python3.8

USER root

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        python3-dev \
        default-libmysqlclient-dev \
        gcc \
        curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy initialization script and set permissions
COPY scripts/init_variables.sh /opt/airflow/scripts/
RUN chmod +x /opt/airflow/scripts/init_variables.sh

USER airflow

# Install Python dependencies
COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /requirements.txt

# Set environment variables
ENV PYTHONPATH=/opt/airflow
ENV AIRFLOW_HOME=/opt/airflow

# Install additional Python packages
RUN pip install --no-cache-dir \
    apache-airflow-providers-mongo \
    pymongo 