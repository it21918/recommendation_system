import time
import json
from random import randint, random

from dataGenerator import generate_user, generate_event, generate_coupon
from kafka import KafkaProducer


def key_ending_partitioner(key, all_partitions, available):
    """
    Custom Kafka partitioner to get the partition based on the ending digit of the key
    :param key: partitioning key
    :param all_partitions: list of all partitions sorted by partition ID
    :param available: list of available partitions in no particular order
    :return: one of the values from all_partitions or available

    creates partitions based on the last digit of the given key
    """

    if key is None:
        if available:
            return random.choice(available)
        return random.choice(all_partitions)

    if isinstance(key, bytes):
        key = key.decode('utf-8')

    ending_digit = int(key[-1])
    idx = ending_digit % len(all_partitions)
    return all_partitions[idx]


# Messages will be serialized as JSON
def serializer(message):
    return json.dumps(message).encode('utf-8')


# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=serializer,
    partitioner=key_ending_partitioner
)

if __name__ == '__main__':
    try:
        counter = randint(0, 9)

        # Infinite loop - runs until you kill the program
        while True:
            print(str(counter).encode('utf-8'))
            producer.send(topic='user', value=generate_user(), key=str(counter).encode('utf-8'))
            print(generate_user())
            producer.send(topic='event', value=generate_event(), key=str(counter).encode('utf-8'))
            print(generate_event())
            producer.send(topic='coupon', value=generate_coupon(), key=str(counter).encode('utf-8'))
            print(generate_coupon())
            counter = counter + 1

            # Sleep for 10sec
            time_to_sleep = 10
            time.sleep(time_to_sleep)
    except KeyboardInterrupt:
        print('Shutting down...')
        producer.close()
