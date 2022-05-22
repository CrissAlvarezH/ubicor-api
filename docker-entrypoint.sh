#!/bin/bash

# Run prestart script
sh prestart.sh

# Start server
uvicorn app.main:app --proxy-headers --host 0.0.0.0 --port 80