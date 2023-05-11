# Используем базовый образ Python
FROM python:3.10.5 AS base

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем зависимости проекта (pyproject.toml и poetry.lock) внутрь контейнера
COPY pyproject.toml poetry.lock ./

# Обновляем pip и устанавливаем poetry
RUN pip install --upgrade pip --no-cache-dir && \
    pip install poetry --no-cache-dir && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi --no-root

# Создаем образ для продакшн сборки
FROM base AS prod

# Копируем все файлы проекта внутрь контейнера
COPY . .

# Устанавливаем только продакшн зависимости через poetry
RUN poetry install --no-dev --no-interaction --no-ansi --no-root


# Создаем образ для запуска в runtime
FROM prod AS runtime

# Устанавливаем несколько переменных окружения, необходимых для работы FastAPI-приложения
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

CMD ["python", "main.py"]
