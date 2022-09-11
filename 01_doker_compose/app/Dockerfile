# Укажите необходимую версию python
FROM python:3.10

# Выберите папку, в которой будут размещаться файлы проекта внутри контейнера 
WORKDIR /

# Заведите необходимые переменные окружения
ENV DJANGO_SETTINGS_MODULE 'config.settings'

# Скопируйте всё оставшееся. Для ускорения сборки образа эту команду стоит разместить ближе к концу файла. 
COPY . .


# Установите зависимости
RUN  pip install --upgrade pip \
     && pip install -r requirements.txt

# RUN  python manage.py migrate
# RUN  python manage.py collectstatic


# python manage.py flush --no-input
# RUN sed -i 's/\r$//g' entrypoint.sh && chmod +x entrypoint.sh
# RUN python manage.py migrate
# RUN python manage.py collectstatic --no-input
# python manage.py create_movies


# Укажите порт, на котором приложение будет доступно внутри Docker-сети
EXPOSE 8000

# CMD python manage.py migrate
# Укажите, как запускать ваш сервис
# ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# ENTRYPOINT ["gunicorn", "config.wsgi:application", "--bind", "0:8000" ]


# CMD python manage.py migrate && python manage.py collectstatic --noinput && gunicorn --bind 0.0.0.0:8000 config.wsgi
CMD python manage.py collectstatic --noinput && python manage.py migrate && python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" && gunicorn --bind 0.0.0.0:8000 config.wsgi
# ENTRYPOINT ["gunicorn", "config.wsgi:application", "--bind", "0:8000" ]