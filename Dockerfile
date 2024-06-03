FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/

RUN apt-get update && apt-get install -y libpq-dev gcc

RUN pip install -r requirements.txt

COPY . /app/


COPY ./entrypoint.sh .
ENTRYPOINT ["sh", "/app/entrypoint.sh"]