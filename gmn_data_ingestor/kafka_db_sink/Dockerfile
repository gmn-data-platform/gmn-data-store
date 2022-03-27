FROM python:3-slim-bullseye

RUN apt-get update && \
    apt-get install -y librdkafka1 \
                       curl \
                       jq \
                       krb5-user \
                       libsasl2-modules-gssapi-mit \
                       librdkafka-dev \
                       libsasl2-dev \
                       libkrb5-dev \
                       libssl-dev \
                       g++
#    apt-get -y remove libkrb5-dev libsasl2-dev librdkafka-dev libssl-dev g++ && \
#    apt-get -y autoremove && \
#    apt-get -y clean

COPY kafka_db_sink.py /app/kafka_db_sink.py
WORKDIR /app

RUN pip install --upgrade pip && pip install gmn-python-api==0.0.3 "confluent-kafka[avro]"==1.8.2 python-dotenv==0.15.0 SQLAlchemy==1.4.31 sqlalchemy-utils==0.38.2 sqlalchemy-json==0.4.0 psycopg2-binary==2.9.3 requests==2.22.0 --no-binary=confluent-kafka

CMD [ "python" , "kafka_db_sink.py" ]