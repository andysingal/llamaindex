# Read variables from .env file
ifneq (,$(wildcard ./.env.dev))
    include .env.dev
    export
endif

ifeq ($(OS),Windows_NT)     # is Windows_NT on XP, 2000, 7, Vista, 10...
    detected_OS := Windows
	DOCKER_PREFIX = docker
else
    detected_OS := $(shell uname)  # same as "uname -s"
	DOCKER_PREFIX = sudo docker
endif

build_backend:
	@echo "Backend image build start : ${BACKEND_CONTAINER_NAME}:${BACKEND_IMAGE_TAG}"
	@cd backend && $(DOCKER_PREFIX) build -t ${BACKEND_CONTAINER_NAME}:${BACKEND_IMAGE_TAG} -f backend.dockerfile .
	@echo "Backend image built: ${BACKEND_CONTAINER_NAME}:${BACKEND_IMAGE_TAG}"

create_network:
	@echo "Creating Docker network: ${DOCKER_COMPOSE_NETWORK_NAME}"
	$(DOCKER_PREFIX) network create ${DOCKER_COMPOSE_NETWORK_NAME}
	@echo "Docker network created: ${DOCKER_COMPOSE_NETWORK_NAME}"

run_backend:
	@echo "Starting backend services"
	$(DOCKER_PREFIX) compose --env-file .env.dev -f docker-compose.backend.dev.yml up

down_backend:
	@echo "Starting other services"
	$(DOCKER_PREFIX) compose --env-file .env.dev -f docker-compose.backend.dev.yml down

run_others:
	@echo "Starting other services"
	$(DOCKER_PREFIX) compose --env-file .env.dev -f docker-compose.dev.yml up -d

down_others:
	@echo "Stopping other services"
	$(DOCKER_PREFIX) compose --env-file .env.dev -f docker-compose.dev.yml down

run_all:
	@echo "Starting all services"
	$(DOCKER_PREFIX) compose --env-file .env.dev -f docker-compose.dev.yml up -d
	$(DOCKER_PREFIX) compose --env-file .env.dev -f docker-compose.backend.dev.yml up

down_all:
	@echo "Stopping all services"
	$(DOCKER_PREFIX) compose --env-file .env.dev -f docker-compose.dev.yml down
	$(DOCKER_PREFIX) compose --env-file .env.dev -f docker-compose.backend.dev.yml down

run_ollama:
	$(DOCKER_PREFIX) compose --env-file .env.dev -f docker-compose.ollama.yml up -d

down_ollama:
	$(DOCKER_PREFIX) compose --env-file .env.dev -f docker-compose.ollama.yml down

init_backend: build_backend create_network