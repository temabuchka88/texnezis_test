# syntax=docker/dockerfile:1

FROM python:alpine

WORKDIR /Bot

COPY . .
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools wheel
RUN pip3 install -r requirements.txt

CMD [ "python3", "bot.py"]
