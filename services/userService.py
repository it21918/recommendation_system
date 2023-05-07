import psycopg2
from flask import jsonify

# Connect to the database
def get_db_connection():
    conn = psycopg2.connect(host='localhost', database='mydb', user="postgres", password="postgres")
    return conn


def createUserTable():
    # Open a cursor to perform database operations
    conn = get_db_connection()
    cur = conn.cursor()

    # Execute a command: this creates a new table
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
                username varchar(50) PRIMARY KEY,
                birth_year integer NOT NULL,
                country varchar(50) NOT NULL,
                currency varchar(50) NOT NULL,
                registration_date timestamp with time zone DEFAULT CURRENT_TIMESTAMP)''')

    # Create the friend table if it doesn't exist
    cur.execute('''CREATE TABLE IF NOT EXISTS friends (
                user_username varchar(50) NOT NULL REFERENCES users(username) ON DELETE CASCADE,
                friend_username varchar(50) NOT NULL REFERENCES users(username) ON DELETE CASCADE,
                PRIMARY KEY (user_username, friend_username));''')

    conn.commit()
    cur.close()
    conn.close()


def insert_user(user):
    createUserTable()
    conn = get_db_connection()
    cur = conn.cursor()

    # Insert the user data into the user table
    cur.execute('INSERT INTO users (username, birth_year, country, currency) '
                'VALUES (%s, %s, %s, %s);', (user['username'], user['birth_year'], user['country'], user['currency']))

    # Insert the user's friends into the friends table
    for friend in user['friends']:
        print(friend)
        cur.execute('INSERT INTO friends (user_username, friend_username) '
                    'VALUES (%s, %s);', (user['username'], friend))

    conn.commit()
    cur.close()
    conn.close()


def delete_user(username):
    createUserTable()
    conn = get_db_connection()
    cur = conn.cursor()

    # Delete the user with the given username from the user table
    cur.execute('DELETE FROM users WHERE username = %s;', (username,))

    conn.commit()
    cur.close()
    conn.close()


def get_user(username):
    createUserTable()
    conn = get_db_connection()
    cur = conn.cursor()

    # Retrieve the user with the given username from the user table
    cur.execute('SELECT * FROM users WHERE username = %s;', (username,))
    row = cur.fetchone()

    if not row:
        cur.close()
        conn.close()
        return jsonify({'error': 'User not found'}), 404

    user = {
        "username": row[0],
        "birth_year": row[1],
        "country": row[2],
        "currency": row[3],
        "registration_date": row[4],
        "friends": []
    }

    # Retrieve the user's friends from the friend table
    cur.execute('''SELECT friend_username FROM friends WHERE user_username=%s''', (row[0],))
    friend_rows = cur.fetchall()
    for friend_row in friend_rows:
        user["friends"].append(friend_row[0])

    cur.close()
    conn.close()

    return user


def get_all_users():
    createUserTable()
    conn = get_db_connection()
    cur = conn.cursor()

    # Retrieve the user with the given username from the user table
    cur.execute('''SELECT * FROM users''')
    rows = cur.fetchall()

    users = []
    for row in rows:
        user = {
            "username": row[0],
            "birth_year": row[1],
            "country": row[2],
            "currency": row[3],
            "registration_date": row[4],
            "friends": []
        }

        # Retrieve the user's friends from the friend table
        cur.execute('''SELECT friend_username FROM friends WHERE user_username=%s''', (row[0],))
        friend_rows = cur.fetchall()
        for friend_row in friend_rows:
            user["friends"].append(friend_row[0])

        users.append(user)

    cur.close()
    conn.close()

    return users
