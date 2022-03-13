SHOW ALL TOPICS;

SET 'auto.offset.reset'='earliest';
SET 'cache.max.bytes.buffering' = '0';


CREATE STREAM IF NOT EXISTS trajectory_summary_raw_stream
WITH (KAFKA_TOPIC='trajectory_summary_raw', VALUE_FORMAT='AVRO');

CREATE STREAM IF NOT EXISTS db_public_trajectory WITH (KAFKA_TOPIC='db.public.trajectory',VALUE_FORMAT='AVRO');
CREATE STREAM IF NOT EXISTS db_public_iau_shower_stream WITH (KAFKA_TOPIC='db.public.iau_shower',VALUE_FORMAT='AVRO');
CREATE STREAM IF NOT EXISTS db_public_station_stream WITH (KAFKA_TOPIC='db.public.station',VALUE_FORMAT='AVRO');
CREATE STREAM IF NOT EXISTS db_public_participating_stream WITH (KAFKA_TOPIC='db.public.participating_station',VALUE_FORMAT='AVRO');

CREATE STREAM IF NOT EXISTS db_flat WITH (KAFKA_TOPIC='db_flat',VALUE_FORMAT='AVRO')

FROM db_public_trajectory;

CREATE SINK CONNECTOR SINK_ELASTIC_1 WITH (
  'connector.class'                     = 'io.confluent.connect.elasticsearch.ElasticsearchSinkConnector',
  'connection.url'                      = 'http://elasticsearch:9200',
  'value.converter'                     = 'io.confluent.connect.avro.AvroConverter',
  'value.converter.schema.registry.url' = 'http://schema-registry:8081',
  'type.name'                           = '_doc',
  'topics'                              = 'trajectory_summary_raw, db.public.trajectory, db.public.iau_shower, db.public.station, db.public.participating_station',
  'key.ignore'                          = 'true',
  'schema.ignore'                       = 'false'
);

--   'transforms'= 'ExtractTimestamp',
--   'transforms.ExtractTimestamp.type'= 'org.apache.kafka.connect.transforms.InsertField$Value',
--   'transforms.ExtractTimestamp.timestamp.field' = 'RATING_TS'
-- CREATE SOURCE CONNECTOR SOURCE_POSTGRES_01 WITH (
--     'connector.class' = 'io.debezium.connector.postgresql.PostgresConnector',
--     'database.hostname' = 'db',
--     'database.port' = '5432',
--     'database.user' = 'test_user',
--     'database.password' = 'pass',
--     'database.dbname' = 'gmn_data_store',
--     'database.server.name' = 'db',
--     'table.include.list' = 'public.trajectory',
--     'database.history.kafka.bootstrap.servers' = 'kafka-broker:29092',
--     'database.history.kafka.topic' = 'loaded' ,
--     'include.schema.changes' = 'false',
-- --     'key.converter'= 'org.apache.kafka.connect.storage.StringConverter',
-- --     'value.converter'= 'io.confluent.connect.avro.AvroConverter',
--     'value.converter'= 'org.apache.kafka.connect.storage.StringConverter',
--     'value.converter.schema.registry.url'= 'http://schema-registry:8081'
-- );
--

-- CREATE STREAM ID NOT EXISTS trajectory_participating_station_stream
-- WITH (KAFKA_TOPIC='trajectory_participating_station', VALUE_FORMAT='AVRO')
-- AS SELECT trajectory_id, station_id AS station_id FROM trajectory_summary_stream
-- EMIT CHANGES;
--
-- CREATE STREAM IF NOT EXISTS transformed_stream WITH (kafka_topic='transformed', value_format='AVRO') FROM
--     (SELECT data STRUCT<>, iau_code BIGINT AS iau_code_id, station_id BIGINT FROM extracted_stream) AS extracted_stream;
-- CREATE STREAM IF NOT EXISTS transformed_failed_stream WITH (kafka_topic='transformed_failed', value_format='AVRO');

-- CREATE TABLE transformed_table (
--     id BIGINT PRIMARY KEY,
--     created_at TIMESTAMP,
--     updated_at TIMESTAMP,
--     data VARCHAR, -- test
--     iau_no BIGINT,
--     iau_code VARCHAR(STRING),
--     num_stat BIGINT,
--     participating_station VARCHAR(STRING)
-- ) WITH (KAFKA_TOPIC='extracted', VALUE_FORMAT='AVRO');
--

--
-- CREATE STREAM IF NOT EXISTS loaded_stream WITH (kafka_topic='loaded', value_format='AVRO') FROM
--     (SELECT * FROM transformed_stream);
-- CREATE STREAM IF NOT EXISTS loaded_failed_stream WITH (kafka_topic='loaded_failed', value_format='AVRO');

SHOW TOPICS EXTENDED;
SHOW STREAMS EXTENDED;

