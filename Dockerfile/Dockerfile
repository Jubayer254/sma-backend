FROM python:3.10.12-alpine

WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Add os packages
RUN apk add --no-cache bash
RUN apk add sudo
RUN apk add --update --no-cache git gcc libc-dev libpq-dev python3-dev freetype-dev libjpeg-turbo-dev
RUN apk add --update --no-cache libpng-dev libffi-dev make automake g++ subversion

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the entire project into the container
COPY apps/ /app/

# Copy the env script into the container
COPY setup-cicd-env/ /app/

RUN bash /app/setup-cicd.sh

RUN adduser -D app
RUN chown -R app:app /app
RUN chmod -R 755 /app