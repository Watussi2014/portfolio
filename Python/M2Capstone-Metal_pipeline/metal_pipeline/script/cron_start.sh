#!/bin/bash

# Source the environment variables
source /etc/environment
export PATH=$PATH:/usr/local/bin

# Run the python backup script
/usr/local/bin/python /app/src/backup.py