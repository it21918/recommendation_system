import json
import threading

from kafka import KafkaConsumer
from userService import insert_user
from eventService import DatabaseConnection

user_count = 0  # Global variable for user count
user_count_lock = threading.Lock()  # Lock to synchronize access to user_count

def save_users(consumerOfUsers):
    """ This method inserts users to database """

    global user_count  # Access the global event count variable

    for message in consumerOfUsers:
        data = json.loads(message.value)
        print(data)
        insert_user(data)

        with user_count_lock:
            user_count += 1

            if user_count == 50:
                # Close the database connection after saving 50 users
                DatabaseConnection.get_instance().get_connection().close()
                break


if __name__ == '__main__':
    consumerOfUsers = KafkaConsumer(
        "user",
        bootstrap_servers='localhost:9092',
        auto_offset_reset='latest'
    )
    save_users(consumerOfUsers)

