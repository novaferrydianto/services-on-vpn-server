FROM python:3.6-slim-buster

WORKDIR /usr/src/app
COPY main.py .
COPY tools.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

CMD python main.py