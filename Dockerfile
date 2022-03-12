FROM python:3.9

RUN mkdir /app
WORKDIR /app/

COPY req.txt .

RUN pip install -r req.txt

COPY . /app
