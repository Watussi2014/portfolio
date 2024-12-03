#!/bin/bash

# Source the environment variables
source /etc/environment
export PATH=$PATH:/usr/local/bin

# Run the python script
/usr/local/bin/python /app/src/main.py