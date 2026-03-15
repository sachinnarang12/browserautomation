#!/bin/bash
# Fix ownership of the data directory (Docker volume mounts as root)
chown -R portal:portal /app/data 2>/dev/null || true

# Ensure edition env vars have defaults (supervisord crashes on missing %(ENV_...)s)
export AUTOMATEPORTAL_EDITION="${AUTOMATEPORTAL_EDITION:-standard}"
export AUTOMATEPORTAL_LICENSE_SECRET="${AUTOMATEPORTAL_LICENSE_SECRET:-not-set}"

# Start supervisord
exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf
