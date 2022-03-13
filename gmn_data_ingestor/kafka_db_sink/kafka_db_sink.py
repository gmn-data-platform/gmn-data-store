import math
import sys

sys.path.insert(0, '/database')
from confluent_kafka.avro import AvroConsumer
from confluent_kafka.avro.serializer import SerializerError

from controller import DatabaseController
from models import Trajectory, Station, ParticipatingStation

c = AvroConsumer({
    'bootstrap.servers': 'kafka-broker:29092',
    'group.id': 'kafkadbsinkgroup',
    'enable.auto.commit': False,
    'schema.registry.url': 'http://schema-registry:8081'})

c.subscribe(['trajectory_summary_raw'])

print("starting")
while True:
    try:
        msg = c.poll(10)

    except SerializerError as e:
        print("Message deserialization failed for {}: {}".format(msg, e))
        break

    if msg is None:
        continue

    if msg.error():
        print("AvroConsumer error: {}".format(msg.error()))
        continue

    msg_value = msg.value()
    for key in msg_value.keys():
        if isinstance(msg_value[key], float) and math.isnan(msg_value[key]):
            msg_value[key] = None
    print("Upserting message: ", msg_value)

    db_controller = DatabaseController()
    try:
        db_controller.insert_trajectory_summary(row_dict=msg_value)
    except Exception as e:
        print("Error inserting trajectory summary: {}".format(e))
        continue
    print("Successfully upserted message")

    c.commit(msg) # commit offset
c.close()