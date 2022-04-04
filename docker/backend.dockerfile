FROM python:3.8
WORKDIR /app

# Install system packages
RUN apt-get update -y 

COPY ./backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt