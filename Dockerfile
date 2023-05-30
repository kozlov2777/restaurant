FROM python:3.11

ENV PYTHONUNBUFFERED 1

RUN mkdir /restaurant
WORKDIR /restaurant

COPY requirements.txt /restaurant/
RUN pip install -r requirements.txt

COPY . /restaurant/