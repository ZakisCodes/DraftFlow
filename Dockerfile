# Use a slim Python image
FROM python:3.12-slim

# 1. Create & switch to your app folder
WORKDIR /workspace

# 2. Copy only requirements first (for better caching)
COPY requirements.txt .

# 3. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt 
# Create a non-root user 'vscode' and give it ownership of /workspace
# Install Python dependencies and set up non-root user in one layer
RUN apt update && apt install -y nano git && \
    useradd -m vscode && \
    mkdir -p /workspace && \
    chown -R vscode:vscode /workspace

# 4. Copy the rest of your code
COPY . .

# Tell Docker to run as that user from here on
USER vscode

# 5. Expose FastAPI’s port
EXPOSE 8000

# 6. Default command: run uvicorn with reload
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--reload"]


# (Optional) Add a healthcheck to ensure the container is healthy
# HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
#   CMD curl -f http://localhost:8000/health || exit 1
# only use in production.


