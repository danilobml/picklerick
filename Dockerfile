FROM python:3.12-slim

WORKDIR /picklerick
COPY . .

RUN pip3 install -U pip
RUN pip3 install -r requirements.txt