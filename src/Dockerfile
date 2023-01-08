FROM python:3.8

WORKDIR /usr/app

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN apt-get update -y && apt-get install -y netcat

ENV PYTHONPATH /usr/app