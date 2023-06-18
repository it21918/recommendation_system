import psycopg2


class DatabaseConnection:
    __instance = None

    @staticmethod
    def get_instance():
        if DatabaseConnection.__instance is None:
            DatabaseConnection()
            createCouponTable()
        return DatabaseConnection.__instance

    def __init__(self):
        if DatabaseConnection.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.__conn = self.__create_connection()
            DatabaseConnection.__instance = self

    def __create_connection(self):
        return psycopg2.connect(host='localhost',
                                database='mydb',
                                user="postgres",
                                password="postgres")

    def get_connection(self):
        return self.__conn


def createCouponTable():
    conn = DatabaseConnection.get_instance().get_connection()
    cur = conn.cursor()

    # Execute commands to create the tables
    cur.execute('''CREATE TABLE IF NOT EXISTS coupons (
                    id SERIAL PRIMARY KEY,
                    timestamp timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
                    username varchar(50) NOT NULL REFERENCES users(username) ON DELETE CASCADE
                )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS selections (
                    coupon_id integer NOT NULL REFERENCES coupons(id) ON DELETE CASCADE,
                    event_id integer NOT NULL REFERENCES events(id) ON DELETE CASCADE,
                    odds float NOT NULL,
                    PRIMARY KEY (coupon_id, event_id)
                )''')

    conn.commit()
    cur.close()



def insert_coupon(coupon):
    conn = DatabaseConnection.get_instance().get_connection()
    cur = conn.cursor()

    # Insert the coupon data into the coupons table
    cur.execute('INSERT INTO coupons (username) VALUES (%s) RETURNING id;', (coupon["username"],))
    coupon_id = cur.fetchone()[0]
    conn.commit()

    # Insert the coupon selections into the selections table
    for selection in coupon["selections"]:
        cur.execute('INSERT INTO selections (coupon_id, event_id, odds) '
                    'VALUES (%s, %s, %s);', (coupon_id, selection["event_id"], selection["odds"]))
        conn.commit()

    cur.close()


def get_all_coupons():
    """Function to retrieve all coupons"""
    conn = DatabaseConnection.get_instance().get_connection()
    cur = conn.cursor()

    # Retrieve all coupons from the coupons table
    cur.execute('SELECT id, username FROM coupons;')
    coupons = []
    for row in cur.fetchall():
        coupon = {"coupon_id": row[0], "user_id": row[1], "selections": []}
        cur.execute('SELECT event_id, odds FROM selections WHERE coupon_id = %s;', (row[0],))
        for selection_row in cur.fetchall():
            coupon["selections"].append({"event_id": selection_row[0], "odds": selection_row[1]})
        coupons.append(coupon)

    cur.close()
    return coupons


def get_coupon(coupon_id):
    """Function to retrieve a specific coupon by coupon_id"""
    conn = DatabaseConnection.get_instance().get_connection()
    cur = conn.cursor()

    # Retrieve the coupon from the coupons table
    cur.execute('SELECT id, username FROM coupons WHERE id = %s;', (coupon_id,))
    row = cur.fetchone()

    if row is None:
        return None

    coupon = {"coupon_id": row[0], "username": row[1], "selections": []}

    # Retrieve the selections associated with the coupon
    cur.execute('SELECT event_id, odds FROM selections WHERE coupon_id = %s;', (coupon_id,))
    for selection_row in cur.fetchall():
        coupon["selections"].append({"event_id": selection_row[0], "odds": selection_row[1]})

    cur.close()
    return coupon


def get_all_user_coupons(username):
    conn = DatabaseConnection.get_instance().get_connection()
    cur = conn.cursor()

    # Retrieve the coupons for the given username, ordered by timestamp
    cur.execute('SELECT id, username FROM coupons WHERE username = %s ORDER BY timestamp;', (username,))
    coupons = []
    for row in cur.fetchall():
        coupon = {"coupon_id": row[0], "user_id": row[1], "selections": []}
        cur.execute('SELECT event_id, odds FROM selections WHERE coupon_id = %s;', (row[0],))
        for selection_row in cur.fetchall():
            coupon["selections"].append({"event_id": selection_row[0], "odds": selection_row[1]})
        coupons.append(coupon)

    cur.close()
    return coupons


def delete_coupon(coupon_id):
    conn = DatabaseConnection.get_instance().get_connection()
    cur = conn.cursor()

    # Delete the coupon and its selections from the database
    cur.execute('DELETE FROM selections WHERE coupon_id = %s;', (coupon_id,))
    cur.execute('DELETE FROM coupons WHERE id = %s;', (coupon_id,))
    conn.commit()

    cur.close()


def get_friends_coupons(friends):
    friends_coupons = []

    for friend in friends:
        friends_coupons.append(get_all_user_coupons(friend))

    return friends_coupons
