# Use the official Nginx image as the base
FROM nginx:1.21-alpine

# Install envsubst (part of the gettext package) for environment variable substitution
RUN apk add --no-cache gettext

# Copy the nginx.conf template
COPY /nginx/nginx.conf /etc/nginx/nginx.conf.template

# Run envsubst to replace variables in nginx.conf before starting Nginx
CMD envsubst '$APP_SERVER_BIND_PORT' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf && nginx -g 'daemon off;'