import time
import json
from dataGenerator import generate_user, generate_event, generate_coupon
from kafka import KafkaProducer


# Messages will be serialized as JSON
def serializer(message):
    return json.dumps(message).encode('utf-8')


# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=serializer
)

if __name__ == '__main__':

    # Infinite loop - runs until you kill the program
    while True:
        producer.send('user', generate_user())
        producer.send('event', generate_event())
        producer.send('coupon', generate_coupon())

        # Sleep for two hours
        time_to_sleep = 3600 * 1000
        time.sleep(time_to_sleep)
