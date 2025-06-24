#!/bin/sh

# Ensure the secret file has correct permissions
# The filename here MUST exactly match the name you gave your secret file in Render.
# Assuming you named it 'GOOGLE_CREDENTIALS_JSON.json' when uploading to Render Secret Files.
chmod 644 /etc/secrets/GOOGLE_CREDENTIALS_JSON.json

# Start the FastAPI application
uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8000}
