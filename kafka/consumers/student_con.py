from kafka import KafkaConsumer
from kafka.config_kafka import KAFKA_BROKER, STUDENTS_TOPIC

consumer = KafkaConsumer(
    STUDENTS_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    group_id='school',
    auto_offset_reset='earliest'
)

for message in consumer:
    print(f"Key: {message.key}, Value: {message.value}")
