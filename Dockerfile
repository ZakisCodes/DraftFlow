
# Use a slim Python image
FROM python:3.12-slim

# 1. Create & switch to your app folder
WORKDIR /workspace

# 2. Copy only requirements first (for better caching)
COPY requirements.txt .

# 3. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt 

# Install Python dependencies and set up non-root user in one layer
RUN apt-get update && apt-get install -y --no-install-recommends \
    nano \
    git \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    fonts-liberation \
    fonts-dejavu-core \
    shared-mime-info \
    gosu \
  && rm -rf /var/lib/apt/lists/* \
  && apt-get clean  \
  && useradd -m vscode \
  && mkdir -p /workspace \
  && chown -R vscode:vscode /workspace

# 4. Copy the rest of your code
COPY . .

# Copy the entrypoint script and make it executable
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Tell Docker to run as that user from here on
USER root

# 5. Expose FastAPI’s port
EXPOSE 8000

# 6. Default command: run the entrypoint script
CMD ["/usr/local/bin/entrypoint.sh"]

# 6. Default command: run uvicorn with reload
#CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--reload"]
#CMD ["sh", "-c", "uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8000}"]



# (Optional) Add a healthcheck to ensure the container is healthy
# HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
#   CMD curl -f http://localhost:8000/health || exit 1
# only use in production.
