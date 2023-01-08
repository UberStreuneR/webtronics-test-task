dc = docker-compose

build:
	docker build ./src -t webtronics_app

run:
	$(dc) up -d api

setup-db:
	$(dc) run --rm api sh -c "./run.sh; alembic upgrade head"

alembic:
	$(dc) run --rm api sh -c "alembic revision --autogenerate -m $(msg); alembic upgrade head"
