CREATE STREAM IF NOT EXISTS extracted_stream WITH (KAFKA_TOPIC='extracted', VALUE_FORMAT='AVRO');
CREATE STREAM IF NOT EXISTS extracted_failed_stream WITH (kafka_topic='extracted_failed', value_format='AVRO');
CREATE STREAM IF NOT EXISTS transformed_stream WITH (kafka_topic='transformed', value_format='AVRO');
CREATE STREAM IF NOT EXISTS transformed_failed_stream WITH (kafka_topic='transformed_failed', value_format='AVRO');
CREATE STREAM IF NOT EXISTS loaded_stream WITH (kafka_topic='loaded', value_format='AVRO');
CREATE STREAM IF NOT EXISTS loaded_failed_stream WITH (kafka_topic='loaded_failed', value_format='AVRO');