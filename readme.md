# Project build and run

- Clone to a local repo

### Without makefile:

- $ docker build ./src -t webtronics_app
- $ docker-compose run --rm api sh -c "./run.sh; alembic upgrade head"
- $ docker-compose up -d api

### With makefile:

- $ make build
- $ make setup-db
- $ make run
