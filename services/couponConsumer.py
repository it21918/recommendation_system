import json
import threading

from kafka import KafkaConsumer
from couponService import insert_coupon
from eventService import DatabaseConnection
from validator import validate_coupon_schema

coupon_count = 0  # Global variable for user count
coupon_count_lock = threading.Lock()  # Lock to synchronize access to user_count

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
    consumerOfCoupons = KafkaConsumer(
        "coupon",
        bootstrap_servers='localhost:9092',
        auto_offset_reset='latest'
    )
    save_coupons(consumerOfCoupons)
