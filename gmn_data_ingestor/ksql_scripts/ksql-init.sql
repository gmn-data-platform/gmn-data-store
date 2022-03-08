-- KSQL ETL
SHOW ALL TOPICS;

CREATE STREAM IF NOT EXISTS extracted_stream WITH (KAFKA_TOPIC='extracted', VALUE_FORMAT='AVRO');
CREATE STREAM IF NOT EXISTS extracted_failed_stream WITH (kafka_topic='extracted_failed', value_format='AVRO');

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
-- CREATE STREAM IF NOT EXISTS transformed_stream WITH (kafka_topic='transformed', value_format='AVRO') FROM
--     (SELECT * FROM extracted_stream) AS extracted_stream;
-- CREATE STREAM IF NOT EXISTS transformed_failed_stream WITH (kafka_topic='transformed_failed', value_format='AVRO');
--
-- CREATE STREAM IF NOT EXISTS loaded_stream WITH (kafka_topic='loaded', value_format='AVRO') FROM
--     (SELECT * FROM transformed_stream);
-- CREATE STREAM IF NOT EXISTS loaded_failed_stream WITH (kafka_topic='loaded_failed', value_format='AVRO');

SHOW TOPICS EXTENDED;
SHOW STREAMS EXTENDED;

