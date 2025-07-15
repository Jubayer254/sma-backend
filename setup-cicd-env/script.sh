#!/bin/bash

# Set local app directory using project-relative path
APP_DIR="./sma_backend/conf"

# Create directory if it doesn't exist
mkdir -p "$APP_DIR"

# Create .env file using environment variables
cat > "$APP_DIR/.env" << EOF
EMAIL_HOST="${EMAIL_HOST}"
EMAIL_PORT="${EMAIL_PORT}"
EMAIL_USE_TLS="${EMAIL_USE_TLS}"
EMAIL_HOST_USER="${EMAIL_HOST_USER}"
EMAIL_HOST_PASSWORD="${EMAIL_HOST_PASSWORD}"
SECRET_KEY="${SECRET_KEY}"
DEBUG=${DEBUG}
ALLOWED_HOSTS="${ALLOWED_HOSTS}"
TEST="${TEST}"
EOF

# Set secure permissions
chmod 600 "$APP_DIR/.env"

echo ".env file created successfully at $APP_DIR/.env"
