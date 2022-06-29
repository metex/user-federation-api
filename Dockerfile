FROM python:3.8-slim-buster

ADD . /code
WORKDIR /code

RUN python3 -m pip install simple_http_server bcrypt mysql-connector-python

EXPOSE 5000
CMD ["python3", "webserver.py"]