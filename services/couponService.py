import psycopg2


# Connect to the database
def get_db_connection():
    conn = psycopg2.connect(host='localhost', database='mydb', user="postgres", password="postgres")
    return conn


def createCouponTable():
    # Open a cursor to perform database operations
    conn = get_db_connection()
    cur = conn.cursor()

    # Execute a command: this creates a new table
    cur.execute('''CREATE TABLE IF NOT EXISTS coupons (
                id SERIAL PRIMARY KEY,
                username varchar(50) NOT NULL REFERENCES users(username) ON DELETE CASCADE
                )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS selections (
                coupon_id integer NOT NULL REFERENCES coupons(id) ON DELETE CASCADE,
                event_id integer NOT NULL REFERENCES events(id) ON DELETE CASCADE,
                odds float NOT NULL,
                PRIMARY KEY (coupon_id, event_id));''')

    conn.commit()
    cur.close()
    conn.close()


def insert_coupon(coupon):
    createCouponTable()
    conn = get_db_connection()
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
    conn.close()


def get_all_user_coupons(username):
    createCouponTable()
    conn = get_db_connection()
    cur = conn.cursor()

    # Retrieve the coupons for the given username
    cur.execute('SELECT id, username FROM coupons WHERE username = %s;', (username,))
    coupons = []
    for row in cur.fetchall():
        coupon = {"coupon_id": row[0], "user_id": row[1], "selections": []}
        cur.execute('SELECT event_id, odds FROM selections WHERE coupon_id = %s;', (row[0],))
        for selection_row in cur.fetchall():
            coupon["selections"].append({"event_id": selection_row[0], "odds": selection_row[1]})
        coupons.append(coupon)

    cur.close()
    conn.close()
    return coupons


def delete_coupon(coupon_id):
    createCouponTable()
    conn = get_db_connection()
    cur = conn.cursor()

    # Delete the coupon and its selections from the database
    cur.execute('DELETE FROM selections WHERE coupon_id = %s;', (coupon_id,))
    cur.execute('DELETE FROM coupons WHERE id = %s;', (coupon_id,))
    conn.commit()

    cur.close()
    conn.close()


def get_friends_coupons(friends):
    friends_coupons = []

    for friend in friends:
        friends_coupons.append(get_all_user_coupons(friend))

    return friends_coupons
