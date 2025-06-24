#!/bin/sh

# This script is designed to be executed initially as root.
# It performs necessary setup tasks (like changing file permissions)
# and then drops privileges to run the main application as a non-root user.

# Ensure the secret file has correct permissions for the 'vscode' user.
# The filename here MUST exactly match the name you gave your secret file in Render.
# Assuming you named it 'GOOGLE_CREDENTIALS_JSON.json' when uploading to Render Secret Files.
echo "Setting permissions for /etc/secrets/GOOGLE_CREDENTIALS_JSON.json..."
chmod 644 /etc/secrets/GOOGLE_CREDENTIALS_JSON.json
echo "Permissions set. Proceeding to start application as vscode user..."

# Execute the main application as the 'vscode' user using gosu.
# 'exec' replaces the current shell process with the uvicorn process,
# which is a good practice for container entrypoints.
exec gosu vscode uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8000}
