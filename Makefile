PROJECT_NAME=robotvsdinosaurs-dev
DOCKER_COMPOSE_EXEC=docker-compose -p $(PROJECT_NAME)
imageName=fastapi-bundle


test:
	@printf "Starting tests \n"
	python -m unittest discover tests
	@printf "\nFinished tests \n"

init:
	$(DOCKER_COMPOSE_EXEC) up -d --build

rebuild:
	$(DOCKER_COMPOSE_EXEC) up -d --build --remove-orphans

stop:
	@printf "Stopping service"
	$(DOCKER_COMPOSE_EXEC) -f docker-compose.yml stop

logs:
	$(DOCKER_COMPOSE_EXEC) -f docker-compose.yml logs -f --tail=100