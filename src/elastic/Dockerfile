FROM python:3.12.4-slim

ADD requirements.txt /src/requirements.txt

WORKDIR /src

RUN apt-get update && pip3 install -r requirements.txt

EXPOSE 9200

ADD main.py /src/main.py
ADD kibanaManagement.py /src/kibanaManagement.py
ADD elasticManagement.py /src/elasticManagement.py
COPY ./config /src/config

CMD python3 main.py