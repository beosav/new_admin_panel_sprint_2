# Укажите необходимую версию python
FROM python:3.7-slim

# Выберите папку, в которой будут размещаться файлы проекта внутри контейнера 
WORKDIR /

# Заведите необходимые переменные окружения
ENV DJANGO_SETTINGS_MODULE 'config.settings'

# Скопируйте всё оставшееся. Для ускорения сборки образа эту команду стоит разместить ближе к концу файла. 
COPY . .


# Установите зависимости
RUN  pip install --upgrade pip \
     && pip install --no-cache-dir -r requirements.txt

# Укажите порт, на котором приложение будет доступно внутри Docker-сети
EXPOSE 8000

CMD python manage.py collectstatic --noinput && python manage.py migrate && python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" && gunicorn --bind 0.0.0.0:8000 config.wsgi
