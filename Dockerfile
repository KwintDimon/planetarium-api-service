FROM python:3.11.6-alpine3.18
LABEL maintainer="dimon@gmail.com"

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    postgresql-dev

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py migrate

RUN adduser \
         --disabled-password \
         --no-create-home \
         my_user

USER my_user
