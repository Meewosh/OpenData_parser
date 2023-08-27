# syntax=docker/dockerfile:1

FROM python:3.10.12-slim-bullseye
RUN echo 'deb http://deb.debian.org/debian testing main' >> /etc/apt/sources.list
RUN apt-get update
RUN apt-get install build-essential -y
ENV HOME /app
WORKDIR /app
COPY . /app/
RUN pip3 install -r /app/requirements.txt
EXPOSE 8000
RUN python update_date_files.py
CMD gunicorn --bind 0.0.0.0:8000 wsgi:app --log-level DEBUG --timeout 0