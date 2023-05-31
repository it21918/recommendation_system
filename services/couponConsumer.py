import json
import multiprocessing

from kafka import KafkaConsumer, TopicPartition
from couponService import insert_coupon
from eventService import DatabaseConnection
from validator import validate_coupon_schema

coupon_count = 0  # Global variable for user count
coupon_count_lock = multiprocessing.Lock()  # Lock to synchronize access to user_count


def save_coupons(consumerOfCoupons):
    """ This method inserts users to database """

    global coupon_count  # Access the global event count variable

    for message in consumerOfCoupons:
        data = json.loads(message.value)
        validate_coupon_schema(data)

        print(data)
        insert_coupon(data)

        with coupon_count_lock:
            coupon_count += 1

            if coupon_count == 50:
                # Close the database connection after saving 50 coupons
                DatabaseConnection.get_instance().get_connection().close()
                break


if __name__ == '__main__':
    partitions012 = [0, 1, 2]  # Specify the partitions to read from
    partitions345 = [3, 4, 5]
    partitions6789 = [6, 7, 8, 9]

    consumer_of_coupons012 = KafkaConsumer(
        bootstrap_servers='localhost:9092',
        auto_offset_reset='latest',
        key_deserializer=lambda key: key.decode('utf-8')
    )
    consumer_of_coupons345 = KafkaConsumer(
        bootstrap_servers='localhost:9092',
        auto_offset_reset='latest',
        key_deserializer=lambda key: key.decode('utf-8')
    )
    consumer_of_coupons6789 = KafkaConsumer(
        bootstrap_servers='localhost:9092',
        auto_offset_reset='latest',
        key_deserializer=lambda key: key.decode('utf-8')
    )

    # Assign the specified partitions to the consumers
    consumer_of_coupons012.assign([TopicPartition("coupon", p) for p in partitions012])
    consumer_of_coupons345.assign([TopicPartition("coupon", p) for p in partitions345])
    consumer_of_coupons6789.assign([TopicPartition("coupon", p) for p in partitions6789])

    # Create separate processes for each consumer
    process012 = multiprocessing.Process(target=save_coupons, args=(consumer_of_coupons012,))
    process345 = multiprocessing.Process(target=save_coupons, args=(consumer_of_coupons345,))
    process6789 = multiprocessing.Process(target=save_coupons, args=(consumer_of_coupons6789,))

    # Start the processes
    process012.start()
    process345.start()
    process6789.start()

    # Wait for the processes to finish
    process012.join()
    process345.join()
    process6789.join()
