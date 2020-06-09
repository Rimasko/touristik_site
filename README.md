README touristik_site
=====================
## ссылка на  [ekva-tour24](https://ekva-tour24.digital) 

# Проект на Django для туристической фирмы

## для запуска необходимо иметь
* Docker
* docker-compose
## Запуск локально

~~~
$ docker-compose up --build -d
~~~

## Для запуска на сервере придется настроить cerbot и nginx для корректной работы и ssl сертификат 
### команда для запука

~~~
$ sudo docker-compose -f docker-compose.nginx.yml up --build -d
~~~
