FROM python:3.8-slim-buster

ADD . /code
WORKDIR /code
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000
CMD ["python3", "webserver.py"]