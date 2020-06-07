FROM python:3.7-slim AS server

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /server
WORKDIR /server

COPY Pipfile /server/
RUN apt-get update && apt-get install -y curl
RUN pip install pipenv && pipenv lock && pipenv install --system
COPY ./ekvatour /server/

