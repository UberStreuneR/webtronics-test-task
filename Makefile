dc = docker-compose

build:
	docker build ./src -t webtronics_app

run:
	$(dc) up -d api

setup-db:
	$(dc) run --rm api alembic upgrade head

alembic:
	$(dc) run --rm api alembic revision --autogenerate -m $(msg)
	$(dc) run --rm api alembic upgrade head