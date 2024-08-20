FROM python:3.11.7

WORKDIR /app/

COPY requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app/

ENV DJANGO_SETTINGS_MODULE=vk_project.settings

CMD [python manage.py runserver 0.0.0.0]
