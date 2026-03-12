FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system deps needed by cryptography / keyring / noVNC / browser
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc libffi-dev \
        xvfb x11vnc xterm \
        novnc websockify \
        procps net-tools \
        supervisor && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies (cached layer unless requirements change)
COPY requirements_v2.txt ./
RUN pip install --no-cache-dir -r requirements_v2.txt

# Copy application code
COPY . .

# Create data directory for runtime secrets (flask key, credential vault, etc.)
RUN mkdir -p /app/data

# Copy supervisor config
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Run as non-root user
RUN groupadd -r portal && useradd -r -g portal -d /app -s /bin/bash portal && \
    chown -R portal:portal /app && \
    mkdir -p /home/portal && chown portal:portal /home/portal

# Expose ports: 5000=webapp, 6080=noVNC
EXPOSE 5000 6080

# Install gunicorn at build time
RUN pip install --no-cache-dir gunicorn

# Use supervisor to manage all processes (Xvfb, VNC, noVNC, gunicorn)
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
