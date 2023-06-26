import json
import multiprocessing

from flask import jsonify
from kafka import KafkaConsumer, TopicPartition
from validator import validate_event_schema
from eventService import insert_event, DatabaseConnection

event_count = 0  # Global variable for event count
event_count_lock = multiprocessing.Lock()  # Lock to synchronize access to event_count


def save_events(consumer):
    """ This method inserts events to the database """
    global event_count  # Access the global event count variable
    for message in consumer:
        data = json.loads(message.value)
        is_valid, response_message = validate_event_schema(data)
        if not is_valid:
            print(response_message)
            return -1

        insert_event(data)
        with event_count_lock:
            event_count += 1
            if event_count == 50:
                # Close the database connection after saving 50 events
                DatabaseConnection.get_instance().get_connection().close()
                break


if __name__ == '__main__':
    partitions012 = [0, 1, 2]  # Specify the partitions to read from
    partitions345 = [3, 4, 5]
    partitions6789 = [6, 7, 8, 9]

    processes = []

    try:
        consumer_of_events012 = KafkaConsumer(
            bootstrap_servers='localhost:9092',
            auto_offset_reset='latest',
            key_deserializer=lambda key: key.decode('utf-8')
        )
        consumer_of_events345 = KafkaConsumer(
            bootstrap_servers='localhost:9092',
            auto_offset_reset='latest',
            key_deserializer=lambda key: key.decode('utf-8')
        )
        consumer_of_events6789 = KafkaConsumer(
            bootstrap_servers='localhost:9092',
            auto_offset_reset='latest',
            key_deserializer=lambda key: key.decode('utf-8')
        )

        # Assign the specified partitions to the consumers
        consumer_of_events012.assign([TopicPartition("event", p) for p in partitions012])
        consumer_of_events345.assign([TopicPartition("event", p) for p in partitions345])
        consumer_of_events6789.assign([TopicPartition("event", p) for p in partitions6789])

        processes.append(multiprocessing.Process(target=save_events, args=(consumer_of_events012,)))
        processes.append(multiprocessing.Process(target=save_events, args=(consumer_of_events345,)))
        processes.append(multiprocessing.Process(target=save_events, args=(consumer_of_events6789,)))

        # Start the processes
        for process in processes:
            process.start()

        # Wait for the processes to finish
        for process in processes:
            process.join()

    except KeyboardInterrupt:
        print('Shutting down...')
        for process in processes:
            process.terminate()

        DatabaseConnection.get_instance().get_connection().close()
