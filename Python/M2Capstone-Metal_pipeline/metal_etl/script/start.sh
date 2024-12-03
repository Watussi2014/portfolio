#!/bin/bash
set -e

# Export environment variables to a file
env | grep -v "PATH" > /etc/environment
echo "PATH=$PATH:/usr/local/bin" >> /etc/environment

# Run the initialization script
python /app/src/init_db.py

# Start cron
cron

# Keep the container running and show cron logs
tail -f /var/log/cron.log