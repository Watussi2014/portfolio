# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install cron
RUN apt-get update && apt-get -y install cron

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

# Copy the cronjob into the cron directory
COPY cronjob /etc/cron.d/cronjob
RUN chmod 0644 /etc/cron.d/cronjob
RUN crontab /etc/cron.d/cronjob

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

WORKDIR /app
COPY . /app

RUN chmod +x ./script/start.sh ./script/cron_start.sh

CMD ["/bin/bash", "-c", "/app/script/start.sh"]

