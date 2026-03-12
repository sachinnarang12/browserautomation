FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered stdout/stderr
# Force keyring to use a null backend (our app uses its own Fernet vault)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring \
    PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers

WORKDIR /app

# Install system deps needed by cryptography / VNC / browser display
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc libffi-dev \
        xvfb x11vnc xterm \
        procps net-tools curl \
        supervisor && \
    rm -rf /var/lib/apt/lists/*

# Install noVNC + websockify from source (Debian packages unreliable on slim)
RUN mkdir -p /opt/novnc/utils/websockify && \
    curl -sL https://github.com/novnc/noVNC/archive/refs/tags/v1.4.0.tar.gz \
        | tar xz --strip-components=1 -C /opt/novnc && \
    curl -sL https://github.com/novnc/websockify/archive/refs/tags/v0.11.0.tar.gz \
        | tar xz --strip-components=1 -C /opt/novnc/utils/websockify && \
    ln -s /opt/novnc/vnc.html /opt/novnc/index.html

# Install Python dependencies (cached layer unless requirements change)
COPY requirements_v2.txt ./
RUN pip install --no-cache-dir -r requirements_v2.txt

# Pre-install Playwright Chromium + its OS dependencies so tasks start instantly
# Install deps first (needs root), then browser to shared path writable by portal user
RUN playwright install-deps chromium

RUN mkdir -p /opt/pw-browsers && \
    playwright install chromium && \
    chmod -R 777 /opt/pw-browsers

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

# Entrypoint fixes volume permissions then starts supervisord
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
