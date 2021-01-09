FROM arm32v7/postgres:9.6

LABEL org.opencontainers.image.authors="PostgreSQL Docker Community, PostGIS Community, Mike Dillon <mike@appropriate.io, Tobias Hargesheimer <docker@ison.ws>" \
	org.opencontainers.image.title="PostgreSQL+PostGIS" \
	org.opencontainers.image.description="Debian with PostgreSQL 9.6 and PostGIS 2.3 on ARM arch" \
	org.opencontainers.image.licenses="MIT" \
	org.opencontainers.image.url="https://hub.docker.com/r/tobi312/rpi-postgresql-postgis" \
	org.opencontainers.image.source="https://github.com/Tob1asDocker/rpi-postgresql-postgis"

ENV POSTGIS_MAJOR 2.3
ENV POSTGIS_VERSION 2.3.*

RUN apt-get update \
      && apt-cache showpkg postgresql-$PG_MAJOR-postgis-$POSTGIS_MAJOR \
      && apt-get install -y --no-install-recommends \
           postgresql-$PG_MAJOR-postgis-$POSTGIS_MAJOR=$POSTGIS_VERSION \
           postgresql-$PG_MAJOR-postgis-$POSTGIS_MAJOR-scripts=$POSTGIS_VERSION \
           postgis=$POSTGIS_VERSION \
           #postgresql-$PG_MAJOR-pgrouting postgresql-$PG_MAJOR-pgrouting-scripts \
           gdal-bin \
      && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /docker-entrypoint-initdb.d
COPY ./initdb-postgis.sh /docker-entrypoint-initdb.d/postgis.sh
COPY ./update-postgis.sh /usr/local/bin
RUN chmod +x /docker-entrypoint-initdb.d/postgis.sh && \
      chmod +x /usr/local/bin/update-postgis.sh

# Open port 5432 so linked containers can see them
EXPOSE 5432
EXPOSE 8000
EXPOSE 587

# Pull base image
FROM python:3.9

#Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
#RUN mkdir -p /usr/src/ClockWeb
WORKDIR /usr/src/ClockWeb

# GDAL Dependencies
RUN apt-get update &&\
    apt-get install -y binutils libproj-dev gdal-bin

# Install dependencies
#  prevent additional virtualenv using flag "--system"
COPY Pipfile Pipfile.lock /usr/src/ClockWeb/
RUN pip install pipenv && pipenv install --system

# Copy project
COPY . /usr/src/ClockWeb

#RUN chmod -R 600 /usr/src/ClockWeb/config/nginx/certs
#RUN ls -la /usr/src/ClockWeb/config/nginx/certs
#RUN cat /usr/src/ClockWeb/config/nginx/ssl-params.conf

# run entrypoint.sh
#ENTRYPOINT ["/home/pi/Projects/ClockWeb/entrypoint.sh"]

# define the default command to run when starting the container
CMD ["gunicorn", "--chdir", "config", "--bind", ":8000", "config.wsgi:application"]
