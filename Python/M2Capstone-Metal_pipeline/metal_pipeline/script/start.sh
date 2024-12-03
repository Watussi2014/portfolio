#!/bin/bash
set -e

# Export environment variables to a file
env | grep -v "PATH" > /etc/environment
echo "PATH=$PATH:/usr/local/bin" >> /etc/environment

# Run the pipeline script
python /app/src/main.py

# Start cron
cron

# Keep the container running and show cron logs
tail -f /var/log/cron.log