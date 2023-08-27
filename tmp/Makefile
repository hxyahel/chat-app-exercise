.PHONY: build run stop migrate

build:
	docker-compose build

run:
	docker-compose up #-d

stop:
	docker-compose down

migrate:
	alembic upgrade head

