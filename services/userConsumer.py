import json
import multiprocessing

from flask import jsonify
from kafka import KafkaConsumer, TopicPartition
from userService import insert_user
from eventService import DatabaseConnection
from validator import validate_user_schema

user_count = 0  # Global variable for user count
user_count_lock = multiprocessing.Lock()  # Lock to synchronize access to user_count


def save_users(consumerOfUsers):
    """ This method inserts users to database """

    global user_count  # Access the global event count variable

    for message in consumerOfUsers:
        data = json.loads(message.value)
        is_valid, response_message = validate_user_schema(data)
        if not is_valid:
            print(response_message)
            return -1

        insert_user(data)
        with user_count_lock:
            user_count += 1
            if user_count == 50:
                # Close the database connection after saving 50 users
                # DatabaseConnection.get_instance().get_connection().close()
                break


if __name__ == '__main__':
    partitions012 = [0, 1, 2]  # Specify the partitions to read from
    partitions345 = [3, 4, 5]
    partitions6789 = [6, 7, 8, 9]

    processes = []

    try:
        consumer_of_users012 = KafkaConsumer(
            bootstrap_servers='localhost:9092',
            auto_offset_reset='latest',
            key_deserializer=lambda key: key.decode('utf-8')
        )
        consumer_of_users345 = KafkaConsumer(
            bootstrap_servers='localhost:9092',
            auto_offset_reset='latest',
            key_deserializer=lambda key: key.decode('utf-8')
        )
        consumer_of_users6789 = KafkaConsumer(
            bootstrap_servers='localhost:9092',
            auto_offset_reset='latest',
            key_deserializer=lambda key: key.decode('utf-8')
        )

        # Assign the specified partitions to the consumers
        consumer_of_users012.assign([TopicPartition("user", p) for p in partitions012])
        consumer_of_users345.assign([TopicPartition("user", p) for p in partitions345])
        consumer_of_users6789.assign([TopicPartition("user", p) for p in partitions6789])

        processes.append(multiprocessing.Process(target=save_users, args=(consumer_of_users012,)))
        processes.append(multiprocessing.Process(target=save_users, args=(consumer_of_users345,)))
        processes.append(multiprocessing.Process(target=save_users, args=(consumer_of_users6789,)))

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
