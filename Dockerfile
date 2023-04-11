FROM python:3.9.13-alpine

COPY ./app /app
COPY gunicorn.sh /app
COPY requirements.txt /app

WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["./gunicorn.sh"]

EXPOSE 5001
