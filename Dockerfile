# VERSION
ARG AIRFLOW_VERSION=2.10.4
ARG PYTHON_VERSION=3.11

FROM apache/airflow:${AIRFLOW_VERSION}-python${PYTHON_VERSION} 

# Create .ssh directory
RUN mkdir -p /home/airflow/.ssh && chmod 700 /home/airflow/.ssh

# Avoid known_hosts when install dependencies
RUN ssh-keyscan github.com >> ~/.ssh/known_hosts

USER root
# Install git and openssh-client to install dependencies
RUN apt-get update && apt-get install -y \
    git \
    openssh-client

# Create private ket with github access and dbt packages
COPY ./.ssh/id_rsa /home/airflow/.ssh/
COPY ./dbt /opt/airflow/dbt
RUN chown airflow:root /home/airflow/.ssh/id_rsa && chmod 600 /home/airflow/.ssh/id_rsa
RUN chown -R airflow:root /opt/airflow/dbt
USER airflow
# Add user to ssh-agent
RUN  eval "$(ssh-agent -s)" && ssh-add ~/.ssh/id_rsa

COPY requirements.txt /
ENV PYTHONPATH="/usr/local/bin/python:/opt/airflow"
RUN pip3 install --upgrade pip
# Install python dependencies from defined enviroment
ARG ZAPS_CORE_ENVIRONMENT=main
ENV ZAPS_CORE_ENVIRONMENT=$ZAPS_CORE_ENVIRONMENT
RUN pip3 install --no-cache-dir -r /requirements.txt
# Install dbt dependencies
#RUN cd /opt/airflow/dbt/zaps_padel && dbt --no-version-check deps