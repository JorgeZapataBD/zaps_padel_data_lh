-include .env
export

COLOUR_GREEN=\033[0;32m
COLOUR_RED=\033[0;31m
COLOUR_BLUE=\033[0;34m
COLOUR_END=\033[0m
# Definición de variables
DOCKER_COMPOSE_FILE=docker-compose.yaml
LOGS_DIR=logs
ZAPS_CORE_ENVIRONMENT ?= main
export AIRFLOW_VAR_ZAPS_PADEL_GCP_CREDENTIALS_PATH := $(shell pwd)/zaps_padel_gcp_credentials.json
export AIRFLOW_UID := 50000
export ZAPS_CORE_ENVIRONMENT := $(ZAPS_CORE_ENVIRONMENT)
# Comando para construir y desplegar los servicios
build-and-up:
	@echo "Verificando si la carpeta $(LOGS_DIR) existe..."
	@if [ ! -d "$(LOGS_DIR)" ]; then \
		echo "Carpeta $(LOGS_DIR) no encontrada. Creando carpeta..."; \
		mkdir -p $(LOGS_DIR); \
	fi
	@echo "Se instalan las dependencias del repositorio commons desde la rama $(ZAPS_CORE_ENVIRONMENT)."
	@echo "Iniciando los servicios con docker compose, en el caso de que no exista alguna imagen se buildea..."
	docker compose -f $(DOCKER_COMPOSE_FILE) build --build-arg ZAPS_CORE_ENVIRONMENT=$(ZAPS_CORE_ENVIRONMENT) --no-cache && docker compose -f $(DOCKER_COMPOSE_FILE) up -d
# Comando para desplegar los servicios
up:
	@echo "Verificando si la carpeta $(LOGS_DIR) existe..."
	@if [ ! -d "$(LOGS_DIR)" ]; then \
		echo "Carpeta $(LOGS_DIR) no encontrada. Creando carpeta..."; \
		mkdir -p $(LOGS_DIR); \
	fi
	@echo "Iniciando los servicios con docker compose, en el caso de que no exista alguna imagen se buildea..."
	docker compose -f $(DOCKER_COMPOSE_FILE) up -d

# Comando para detener y eliminar los contenedores de docker compose
down:
	@echo "Deteniendo y eliminando contenedores..."
	docker compose -f $(DOCKER_COMPOSE_FILE) down

install:
	@if [ ! -d ".venv" ]; then \
		python3.11 -m venv .venv && \
		echo "Entorno virtual creado."; \
		. .venv/bin/activate && \
		pip3 install apache-airflow==2.10.4 && \
		pip3 install apache-airflow-providers-google==11.0.0 && \
		pip3 install -r requirements.txt && \
		pip3 install pre-commit && \
		pre-commit install; \
	else \
		echo "El entorno virtual ya existe."; \
	fi
	@echo "*** Current venv version is $(COLOUR_GREEN)${VIRTUAL_ENV}${COLOUR_END}"

format: install
	pre-commit run --all-files

.PHONY: tests
tests: install
	@echo "$(COLOUR_GREEN)${PYTHONPATH}$(COLOUR_END)"
	pytest --disable-warnings -v tests/

dbt_test: install
	dbt parse --project-dir $(shell pwd)/dbt/zaps_padel --profiles-dir $(shell pwd)/dbt/zaps_padel --profile zaps_padel
	dbt compile --project-dir $(shell pwd)/dbt/zaps_padel --profiles-dir $(shell pwd)/dbt/zaps_padel --profile zaps_padel