import json
import threading

from kafka import KafkaConsumer
from eventService import insert_event, DatabaseConnection
from validator import validate_event_schema

event_count = 0  # Global variable for event count
event_count_lock = threading.Lock()  # Lock to synchronize access to event_count

def save_events(consumerOfEvents):
    """ This method inserts events to the database """

    global event_count  # Access the global event count variable

    for message in consumerOfEvents:
        data = json.loads(message.value)
        print(data)
        validate_event_schema(data)
        insert_event(data)

        with event_count_lock:
            event_count += 1

            if event_count == 50:
                # Close the database connection after saving 50 events
                DatabaseConnection.get_instance().get_connection().close()
                break


if __name__ == '__main__':

    consumerOfEvents = KafkaConsumer(
        "event",
        bootstrap_servers='localhost:9092',
        auto_offset_reset='latest'
    )
    save_events(consumerOfEvents)