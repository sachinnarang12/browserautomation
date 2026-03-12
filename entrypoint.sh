#!/bin/bash
# Fix ownership of the data directory (Docker volume mounts as root)
chown -R portal:portal /app/data 2>/dev/null || true

# Start supervisord
exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf
