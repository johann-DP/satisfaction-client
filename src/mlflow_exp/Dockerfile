
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
COPY scripts/ /app/scripts

RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y openjdk-17-jdk-headless netcat-openbsd

RUN python -m nltk.downloader stopwords
RUN chmod +x /app/scripts/*.sh

# Installation de Spark
COPY spark.tgz .
RUN tar xzvf spark.tgz && mv spark-3.5.0-bin-hadoop3/ /opt/spark && rm spark.tgz
ENV SPARK_HOME /opt/spark
ENV PATH $SPARK_HOME/bin:$SPARK_HOME/sbin:$PATH
RUN export PYTHONPATH=$(ZIPS="$SPARK_HOME"/python/lib/*.zip; IFS=:; echo "${ZIPS[*]}"):$PYTHONPATH

EXPOSE 5000

CMD ["/app/scripts/start_all.sh"]