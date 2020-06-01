PROJECT_NAME=ethservice

# colors
GREEN = $(shell tput -Txterm setaf 2)
YELLOW = $(shell tput -Txterm setaf 3)
WHITE = $(shell tput -Txterm setaf 7)
RESET = $(shell tput -Txterm sgr0)
GRAY = $(shell tput -Txterm setaf 6)
TARGET_MAX_CHAR_NUM = 20

# Common

all: run

## Runs application. Builds, creates, starts, and attaches to containers for a service. | Common
run:
	@docker-compose up

## Rebuild templateaio_app container
build:
	@docker-compose build

## Stops application. Stops running container without removing them.
stop:
	@docker-compose stop

## Removes stopped service containers.
clean:
	@docker-compose down

## Runs command `bash` commands in docker container.
bash:
	@docker exec -it $(PROJECT_NAME) bash

# Help

## Shows help.
help:
	@echo ''
	@echo 'Usage:'
	@echo ''
	@echo '  ${YELLOW}make${RESET} ${GREEN}<target>${RESET}'
	@echo ''
	@echo 'Targets:'
	@awk '/^[a-zA-Z\-]+:/ { \
		helpMessage = match(lastLine, /^## (.*)/); \
		if (helpMessage) { \
		    if (index(lastLine, "|") != 0) { \
				stage = substr(lastLine, index(lastLine, "|") + 1); \
				printf "\n ${GRAY}%s: \n\n", stage;  \
			} \
			helpCommand = substr($$1, 0, index($$1, ":")-1); \
			helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
			if (index(lastLine, "|") != 0) { \
				helpMessage = substr(helpMessage, 0, index(helpMessage, "|")-1); \
			} \
			printf "  ${YELLOW}%-$(TARGET_MAX_CHAR_NUM)s${RESET} ${GREEN}%s${RESET}\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)
	@echo ''

# Docs

# Linters & tests

## Formats code with `black`. | Linters
black:
	@docker-compose run --rm $(PROJECT_NAME)_app black $(PROJECT_NAME) --exclude $(PROJECT_NAME)/migrations -l 79

## Run dev.
dev:
	@cd ./api;gunicorn -w 1 main:app --bind 0.0.0.0:7999 --worker-class aiohttp.worker.GunicornUVLoopWebWorker --timeout 3600 --graceful-timeout 3600  --access-logfile '-'

## Formats code with `flake8`.
lint:
	@docker-compose run --rm $(PROJECT_NAME)_app flake8 $(PROJECT_NAME)

## Runs tests. | Tests
test: lint
	@docker-compose up test
	@docker-compose stop test

workerui:
	@celery flower --broker=redis://:redis@localhost:6380/15


worker:
	@cd ./api;celery -A worker worker -l info
## Runs application with specified postgres and redis.
wait_resources:
	python3 -m $(PROJECT_NAME).utils.wait_script
