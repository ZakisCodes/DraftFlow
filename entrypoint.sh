#!/bin/sh

# This script runs initially as 'root' to handle setup tasks,
# then drops privileges to run the main application as 'vscode'.

echo "Entrypoint script starting..."

# Define the path to your secret file and the name of the environment variable
SECRET_FILE_PATH="/etc/secrets/GOOGLE_CREDENTIALS_JSON.json"
ENV_VAR_NAME="FIREBASE_SERVICE_ACCOUNT_JSON" # New environment variable to hold the JSON content

# Check if the secret file exists
if [ ! -f "$SECRET_FILE_PATH" ]; then
    echo "ERROR: Secret file not found at '$SECRET_FILE_PATH'. Please ensure it's uploaded as a Render Secret File with the correct filename."
    exit 1
fi

# Read the content of the secret file while still running as root.
# This content will be stored in the new environment variable.
echo "Reading Firebase credentials from '$SECRET_FILE_PATH' and exporting to '$ENV_VAR_NAME'..."
FIREBASE_JSON_CONTENT=$(cat "$SECRET_FILE_PATH")

# Export the content as an environment variable.
# The 'export' command makes this variable available to child processes (like uvicorn).
export "$ENV_VAR_NAME"="$FIREBASE_JSON_CONTENT"
echo "Environment variable '$ENV_VAR_NAME' has been set."

# Execute the main application as the 'vscode' user using gosu.
# The application will now read the credentials from the environment variable we just set.
echo "Starting FastAPI application as 'vscode' user..."
exec gosu vscode uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8000}
