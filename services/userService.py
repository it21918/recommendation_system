import psycopg2
from flask import jsonify


class DatabaseConnection:
    __instance = None

    @staticmethod
    def get_instance():
        """ Static method to get the singleton instance """
        if DatabaseConnection.__instance is None:
            DatabaseConnection()
            createUserTable()
        return DatabaseConnection.__instance

    def __init__(self):
        """ Private constructor """
        if DatabaseConnection.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.__conn = self.__connect()
            DatabaseConnection.__instance = self

    def __connect(self):
        """ Connect to the database """
        conn = psycopg2.connect(host='localhost', database='mydb', user="postgres", password="postgres")
        return conn

    def get_connection(self):
        """ Get the database connection """
        return self.__conn


def createUserTable():
    conn = DatabaseConnection.get_instance().get_connection()
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


def insert_user(user):
    conn = DatabaseConnection.get_instance().get_connection()
    cur = conn.cursor()

    # Insert the user data into the user table
    cur.execute('INSERT INTO users (username, birth_year, country, currency) '
                'VALUES (%s, %s, %s, %s);', (user['username'], user['birth_year'], user['country'], user['currency']))

    # Insert the user's friends into the friends table
    for friend in user['friends']:
        cur.execute('INSERT INTO friends (user_username, friend_username) '
                    'VALUES (%s, %s);', (user['username'], friend))

    conn.commit()
    cur.close()


def delete_user(username):
    conn = DatabaseConnection.get_instance().get_connection()
    cur = conn.cursor()

    # Delete the user with the given username from the user table
    cur.execute('DELETE FROM users WHERE username = %s;', (username,))

    conn.commit()
    cur.close()


def get_user(username):
    conn = DatabaseConnection.get_instance().get_connection()
    cur = conn.cursor()

    # Retrieve the user with the given username from the user table
    cur.execute('SELECT * FROM users WHERE username = %s;', (username,))
    row = cur.fetchone()

    # Retrieve the user's friends from the friend table
    cur.execute('''SELECT friend_username FROM friends WHERE user_username=%s''', (row[0],))
    friend_rows = cur.fetchall()

    if not row:
        cur.close()
        return jsonify({'error': 'User not found'}), 404

    user = {
        "username": row[0],
        "birth_year": row[1],
        "country": row[2],
        "currency": row[3],
        "registration_date": row[4].strftime("%Y-%m-%dT%H:%M:%S"),
        "friends": friend_rows
    }

    cur.close()
    return user


def get_all_users():
    conn = DatabaseConnection.get_instance().get_connection()
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
            "registration_date": row[4].strftime("%Y-%m-%dT%H:%M:%S"),
            "friends": []
        }

        # Retrieve the user's friends from the friend table
        cur.execute('''SELECT friend_username FROM friends WHERE user_username=%s''', (row[0],))
        friend_rows = cur.fetchall()
        for friend_row in friend_rows:
            user["friends"].append(friend_row[0])

        users.append(user)

    cur.close()

    return users
