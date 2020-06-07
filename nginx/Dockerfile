FROM python:3.7-slim AS server

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /server
WORKDIR /server

COPY Pipfile /server/
RUN pip install pipenv && pipenv lock && pipenv install --system
COPY ./ekvatour /server/


RUN python ./manage.py collectstatic --noinput

#########################################

FROM nginx:1.13

RUN rm -v /etc/nginx/nginx.conf
COPY ./nginx/nginx.conf /etc/nginx/

RUN mkdir /nginx
COPY --from=server /server/staticfiles /nginx/static
COPY --from=server /server/mediafiles /nginx/media