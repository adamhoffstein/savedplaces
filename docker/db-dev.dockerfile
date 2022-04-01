FROM postgres:14.1-alpine
COPY ./docker/init.sql /docker-entrypoint-initdb.d/