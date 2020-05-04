FROM python:3.8.0-slim

# Set env variables

ENV PYTHONUNBUFFERED 1
ENV HOME=/home/homestream
ENV APP_HOME=/home/homestream/web

# Install dependencies

RUN apt-get update && apt-get install -y ffmpeg netcat gcc libmagic-dev

# User creation

RUN mkdir -p ${HOME}
RUN adduser --system --home=${HOME} \
    --no-create-home --disabled-password --group \
    homestream

RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# Create directories for files used by django.
# Static files are placed here in runserver.sh
# Media files are placed here dynamically
RUN mkdir -p /var/www/homestream/static/ && \
    mkdir -p /var/www/homestream/media/ && \
    mkdir -p /var/log/homestream && \
    chown -R homestream:homestream /var/www/homestream && \
    chown -R homestream:homestream /var/log/homestream


# pip

RUN pip install --upgrade pip
COPY requirements.txt ${APP_HOME}/requirements.txt
RUN pip install -r requirements.txt

# Copy application files

COPY . $APP_HOME
RUN chown -R homestream:homestream $APP_HOME


USER homestream


ENTRYPOINT ["/home/homestream/web/runserver.sh"]
