FROM python:3.12-slim

WORKDIR /picklerick
COPY . .

RUN apt-get update 

RUN pip3 install -U pip
RUN pip3 install -r requirements.txt