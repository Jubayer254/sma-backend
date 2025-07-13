#!/bin/bash

# Create directory if it doesn't exist
mkdir -p /app/sma_backend/conf

# Create .env file using GitHub environment variables
cat > /app/sma_backend/conf/.env << EOF
EMAIL_HOST=${EMAIL_HOST}
EMAIL_PORT=${EMAIL_PORT}
EMAIL_USE_TLS=${EMAIL_USE_TLS}
EMAIL_HOST_USER="${EMAIL_HOST_USER}"
EMAIL_HOST_PASSWORD="${EMAIL_HOST_PASSWORD}"
SECRET_KEY="${SECRET_KEY}"
DEBUG=${DEBUG:-0}
ALLOWED_HOSTS="${ALLOWED_HOSTS}"
TEST="${TEST}"
EOF

# Set secure permissions
chmod 600 /app/sma_backend/conf/.env

echo ".env file created successfully at /app/sma_backend/conf/.env"