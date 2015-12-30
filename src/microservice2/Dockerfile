FROM php:5.6


RUN apt-get update 
RUN apt-get install -y libcurl4-openssl-dev pkg-config
RUN apt-get install -y php5-mongo
RUN pecl install mongodb

ADD microservice2 microservice2
ADD src src
ADD vendor vendor
ADD web web
ADD composer.json composer.json
ADD composer.lock compoer.lock

CMD php -S 0.0.0.0:1339 -t web src/index.php > foo.log

EXPOSE 1339
