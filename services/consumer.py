import json
import threading

from kafka import KafkaConsumer
from userService import insert_user
from eventService import insert_event


def save_events():
    """ This method inserts events to database """

    for message in consumerOfEvents:
        data = json.loads(message.value)
        print(data)
        insert_event(data)


def save_users():
    """ This method inserts users to database """

    for message in consumerOfUsers:
        data = json.loads(message.value)
        print(data)
        insert_user(data)


if __name__ == '__main__':
    consumerOfUsers = KafkaConsumer(
        "user",
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest'
    )

    consumerOfEvents = KafkaConsumer(
        "event",
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest'
    )

    t1 = threading.Thread(target=save_users)
    t2 = threading.Thread(target=save_events)

    t1.start()
    t2.start()
