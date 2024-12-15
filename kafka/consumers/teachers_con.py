from kafka import KafkaConsumer
from kafka.config_kafka import KAFKA_BROKER, TEACHES_TOPIC

consumer = KafkaConsumer(
    TEACHES_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    group_id='school',
    auto_offset_reset='earliest'
)

for message in consumer:
    print(f"Key: {message.key}, Value: {message.value}")
