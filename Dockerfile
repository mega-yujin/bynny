#FROM alpine:latest
FROM python:3.9.13-alpine
COPY . /bynny
#ENV key value
WORKDIR /bynny
RUN pip install -r requirements.txt
#CMD ["python3", "main.py"]
ENTRYPOINT ["./gunicorn.sh"]
EXPOSE 5001
