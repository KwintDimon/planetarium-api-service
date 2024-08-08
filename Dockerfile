# Используем python:3.11.6-alpine3.18 как базовый образ
FROM python:3.11.6-alpine3.18
LABEL maintainer="dimon@gmail.com"

# Обновляем ключ ENV до правильного формата
ENV PYTHONUNBUFFERED=1

# Устанавливаем рабочую директорию с абсолютным путем
WORKDIR /app

# Устанавливаем зависимости для сборки
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    postgresql-dev

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта
COPY . .

# Выполняем миграции
RUN python manage.py migrate

# Команда по умолчанию для запуска приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
