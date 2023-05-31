import json
import multiprocessing
from kafka import KafkaConsumer, TopicPartition
from eventService import insert_event, DatabaseConnection

event_count = 0  # Global variable for event count
event_count_lock = multiprocessing.Lock()  # Lock to synchronize access to event_count


def save_events(consumer):
    """ This method inserts events to the database """
    global event_count  # Access the global event count variable
    for message in consumer:
        data = json.loads(message.value)
        print(data)
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

    # Create separate processes for each consumer
    process012 = multiprocessing.Process(target=save_events, args=(consumer_of_events012,))
    process345 = multiprocessing.Process(target=save_events, args=(consumer_of_events345,))
    process6789 = multiprocessing.Process(target=save_events, args=(consumer_of_events6789,))

    # Start the processes
    process012.start()
    process345.start()
    process6789.start()

    # Wait for the processes to finish
    process012.join()
    process345.join()
    process6789.join()
