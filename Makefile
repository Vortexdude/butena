.PHONY: build up

build:
    docker build -t butena .

up:
    docker-compose up