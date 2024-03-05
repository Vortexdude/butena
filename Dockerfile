FROM python:3.11-bullseye

WORKDIR /app/

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app


COPY ./alembic.ini /app/

COPY ./prestart.sh /app/

COPY ./app /app/app
COPY ./alembic /app/alembic

CMD ["bash", "prestart.sh"]
