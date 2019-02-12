FROM python:3.6
ENV PYTHONUNBUFFERED 1

RUN mkdir /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app
RUN pip install -r requirements.txt

COPY . /usr/src/app