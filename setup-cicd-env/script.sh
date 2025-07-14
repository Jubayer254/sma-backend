#!/bin/bash

# Set local app directory using project-relative path
APP_DIR="./sma_backend/conf"

# Create directory if it doesn't exist
mkdir -p "$APP_DIR"

# Create .env file
cat > ./sma_backend/conf/.env << EOF
EMAIL_HOST=${{ vars.EMAIL_HOST }}
EMAIL_PORT=${{ vars.EMAIL_PORT }}
EMAIL_USE_TLS=${{ vars.EMAIL_USE_TLS }}
EMAIL_HOST_USER=${{ vars.EMAIL_HOST_USER }}
EMAIL_HOST_PASSWORD=${{ secrets.EMAIL_HOST_PASSWORD }}
SECRET_KEY=${{ secrets.SECRET_KEY }}
DEBUG=${{ vars.DEBUG }}
ALLOWED_HOSTS=${{ vars.ALLOWED_HOSTS }}
TEST=${{ vars.TEST }}
EOF

# Set secure permissions
chmod 600 "$APP_DIR/.env"

echo ".env file created successfully at $APP_DIR/.env"