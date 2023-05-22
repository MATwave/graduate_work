# Определение переменных
ADMIN_PANEL_DOCKER_COMPOSE_FILE = -f admin_panel/docker-compose.yml
ASYNC_API_COMPOSE_FILE = async_api/docker-compose.yml
ASYNC_API_TEST_COMPOSE_FILE = async_api/tests/functional/docker-compose.yml
ETL_COMPOSE_FILE = ETL/docker-compose.yml
ASSISTANT_COMPOSE_FILE = assistant_handler/docker-compose.yml
# Запуск контейнеров Docker и выполнение необходимых команд внутри контейнера
admin_panel_up:
	cp .env.template .env

	# Запуск контейнеров Docker в фоновом режиме и перестройка образов, если необходимо
	@echo "Starting containers..."
	docker-compose $(ADMIN_PANEL_DOCKER_COMPOSE_FILE) up -d --build || \
		(echo "Failed to start containers" && exit 1)
	# Ожидание, пока контейнер admin_panel станет здоровым
	@echo "Waiting for admin_panel container to become healthy..."
	until [ "$$(docker inspect -f '{{.State.Health.Status}}' admin_panel)" = "healthy" ]; do \
		sleep 1; \
	done

	# Выполнение миграций базы данных внутри контейнера
	@echo "Running migrations..."
	docker exec -i admin_panel bash -c "python manage.py migrate" || \
		(echo "Failed to run migrations" && exit 1)

	# Сбор статических файлов
	@echo "Collecting static files..."
	docker exec -i admin_panel bash -c "python manage.py collectstatic" || \
		(echo "Failed to collect static files" && exit 1)

	# Создание суперпользователя
	@echo "Creating superuser..."
	docker exec -i admin_panel python  manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin')"  && \
    echo "Superuser created successfully." || \
    (echo "Failed to create superuser" && exit 1)

# Остановка и удаление контейнеров Docker
admin_panel_down:
	@echo "Stopping and removing containers..."
	docker-compose $(ADMIN_PANEL_DOCKER_COMPOSE_FILE) down -v

# Заполнение базы данных из файла SQLite
admin_panel_fill_db:
	@echo "Loading data into Postgres from SQLite file..."
	docker exec -i admin_panel bash -c "cd sqlite_to_postgres && python load_data.py && python tests.py" && \
	echo "The data has been successfully migrated."

admin_panel_test_fill:
	@echo "Testing data migration from SQLite to PostgreSQL"
	docker exec -i admin_panel bash -c "cd sqlite_to_postgres && python tests.py"

#-----------------------------

async_api_up:
	@echo "Copying .env.template to .env"
	cp .env.template .env
	@echo "Starting async_api containers"
	docker-compose -f $(ASYNC_API_COMPOSE_FILE) up -d --build

async_api_down:
	@echo "Stopping async_api containers"
	docker-compose -f $(ASYNC_API_COMPOSE_FILE) down -v

async_api_test_up:
	@echo "Starting async_api test containers"
	docker-compose -f $(ASYNC_API_TEST_COMPOSE_FILE) up -d --build
	@echo "Displaying test logs"
	docker-compose -f $(ASYNC_API_TEST_COMPOSE_FILE) logs -f --tail=0 tests

async_api_test_down:
	@echo "Stopping async_api test containers"
	docker-compose -f $(ASYNC_API_TEST_COMPOSE_FILE) down -v

#-----------------------------

etl_up:
	@echo "Copying .env.template to .env"
	cp .env.template .env
	@echo "creating external networks if it doesn't exist..."
	if [ -z "$$(docker network ls -q -f name=psql_external_network)" ]; then docker network create psql_external_network; fi
	if [ -z "$$(docker network ls -q -f name=es_external_network)" ]; then docker network create es_external_network; fi
	@echo "Starting etl containers"
	docker-compose -f $(ETL_COMPOSE_FILE) up -d --build

etl_down:
	@echo "Stopping etl containers"
	docker-compose -f $(ETL_COMPOSE_FILE) down -v

#-------------------------------

assistants_up:
	@echo "Copying .env.template to .env"
	cp .env.template .env
	@echo "creating external network if it doesn't exists..."
	if [ -z "$$(docker network ls -q -f name=es_external_network)" ]; then docker network create es_external_network; fi
	@echo "Starting assistant containers"
	docker-compose -f $(ASSISTANT_COMPOSE_FILE) up -d --build

assistants_down:
	@echo "Stopping assistant containers"
	docker-compose -f $(ASSISTANT_COMPOSE_FILE) down -v

assistants_tests_run:
	@echo "Running assistant tests"
	docker exec -i assistant_handler bash -c "pytest --disable-warnings ."


#-------------------------------

all_down:
	make admin_panel_down
	make async_api_down
	make etl_down
	make assistants_down

all_up:
	make admin_panel_up
	make admin_panel_fill_db
	make async_api_up
	make etl_up
	make assistants_up
