SHOW ALL TOPICS;

CREATE STREAM IF NOT EXISTS trajectory_summary_stream
WITH (KAFKA_TOPIC='trajectory_summary', VALUE_FORMAT='AVRO');

CREATE STREAM IF NOT EXISTS trajectory_summary_failed_stream
WITH (KAFKA_TOPIC='trajectory_summary_failed', VALUE_FORMAT='JSON');

CREATE SINK CONNECTOR SINK_ELASTIC_1 WITH (
  'connector.class'                     = 'io.confluent.connect.elasticsearch.ElasticsearchSinkConnector',
  'connection.url'                      = 'http://elasticsearch:9200',
  'value.converter'                     = 'io.confluent.connect.avro.AvroConverter',
  'value.converter.schema.registry.url' = 'http://schema-registry:8081',
  'type.name'                           = '_doc',
  'topics'                              = 'trajectory_summary',
  'key.ignore'                          = 'true',
  'schema.ignore'                       = 'false'
);


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

