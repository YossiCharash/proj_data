
from confluent_kafka import Consumer

from database.elasticsearch.elasticsearch_repo import insert_data
from kaf.config_kafka import KAFKA_BROKER,  REVIEWS_TOPIC

consumer_conf = {

    'bootstrap.servers': KAFKA_BROKER,
    'group.id': 'school',
    'auto.offset.reset': 'earliest',
}

consumer = Consumer(consumer_conf)
consumer.subscribe([REVIEWS_TOPIC])

def send_message():
    try:
        while True:
            message = consumer.poll(timeout=1.0)
            if message is None:
                continue

            if message.error():
                print(f"Error: {message.error()}")
                continue

            data = message.value().decode('utf-8')
            print("The data com and insert to database")
            print(data)
            insert_data(data)


    except KeyboardInterrupt:
        print("Process interrupted by user.")

    finally:
        consumer.close()
        print("Consumer closed.")

if __name__ == '__main__':
    send_message()