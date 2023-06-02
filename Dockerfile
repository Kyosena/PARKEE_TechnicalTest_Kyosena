FROM python:3.8-slim-buster

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0
#update pip
RUN pip install --upgrade pip
# install psycopg2
RUN apt-get update \
    && apt install build-essential -y\
    && apt-get install python3-dev musl-dev -y\
    && apt-get install sqlite3 libsqlite3-dev -y\
    && pip install psycopg2-binary

# install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt


# copy project
COPY . /app
RUN mkdir -p static
RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput
RUN adduser myuser

#copy entrypoint
RUN chmod +x entrypoint.sh
RUN ./entrypoint.sh





# run gunicorn
CMD gunicorn parkee.wsgi:application --bind 0.0.0.0:8000