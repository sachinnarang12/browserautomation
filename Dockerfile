FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system deps needed by cryptography / keyring
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libffi-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies (cached layer unless requirements change)
COPY requirements_v2.txt ./
RUN pip install --no-cache-dir -r requirements_v2.txt

# Copy application code
COPY . .

# Create data directory for runtime secrets (flask key, credential vault, etc.)
RUN mkdir -p /app/data

# Run as non-root user
RUN groupadd -r portal && useradd -r -g portal -d /app portal && \
    chown -R portal:portal /app
USER portal

EXPOSE 5000

# Use a proper WSGI server for production; fall back to Flask dev server
# Install gunicorn at build time
RUN pip install --no-cache-dir gunicorn

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--threads", "4", \
     "--timeout", "120", "agent_dashboard_v2:app"]
