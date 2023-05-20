import psycopg2


class DatabaseConnection:
    __instance = None

    @staticmethod
    def get_instance():
        if DatabaseConnection.__instance is None:
            DatabaseConnection()
            createEventTable()
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


# Connect to the database
def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='mydb',
                            user="postgres",
                            password="postgres")
    return conn


def createEventTable():
    conn = DatabaseConnection.get_instance().get_connection()
    cur = conn.cursor()

    # Execute a command: this creates a new table
    cur.execute('''CREATE TABLE IF NOT EXISTS events (
                id SERIAL PRIMARY KEY,
                begin_timestamp timestamp with time zone,
                country varchar(50),
                end_timestamp timestamp with time zone NOT NULL,
                league varchar(50) NOT NULL,
                sport varchar(50) NOT NULL)'''
                )

    cur.execute('''CREATE TABLE IF NOT EXISTS participants (
                username varchar(50) NOT NULL,
                event_id integer NOT NULL REFERENCES events(id) ON DELETE CASCADE,
                PRIMARY KEY (username, event_id));'''
                )

    conn.commit()
    cur.close()


def insert_event(event):
    conn = DatabaseConnection.get_instance().get_connection()
    cur = conn.cursor()

    # Insert the event data into the events table
    cur.execute('INSERT INTO events (begin_timestamp, country, end_timestamp, league, sport) '
                'VALUES (%s, %s, %s, %s, %s) RETURNING id;',
                (event['begin_timestamp'], event['country'], event['end_timestamp'], event['league'], event['sport']))
    event_id = cur.fetchone()[0]
    conn.commit()

    # Insert the event participants into the participants table
    for participant in event['participants']:
        cur.execute('INSERT INTO participants (username, event_id) '
                    'VALUES (%s, %s);', (participant, event_id))
        conn.commit()

    cur.close()


def delete_event(id):
    conn = DatabaseConnection.get_instance().get_connection()
    cur = conn.cursor()

    # Delete the user with the given username from the user table
    cur.execute('DELETE FROM events WHERE id = %s;', (id,))

    conn.commit()
    cur.close()


def get_event(id):
    conn = DatabaseConnection.get_instance().get_connection()
    cur = conn.cursor()

    # Retrieve the user with the given username from the user table
    cur.execute('SELECT * FROM events WHERE id = %s;', (id,))
    user = cur.fetchone()

    cur.close()

    return user


def get_all_events():
    conn = DatabaseConnection.get_instance().get_connection()
    cur = conn.cursor()

    # Retrieve all events from the events table
    cur.execute('''SELECT * FROM events''')
    rows = cur.fetchall()

    events = []
    for row in rows:
        # Create an event dictionary with the event data
        event = {
            "id": row[0],
            "begin_timestamp": row[1],
            "country": row[2],
            "end_timestamp": row[3],
            "league": row[4],
            "sport": row[5],
            "participants": []
        }

        # Retrieve the event's participants from the participants table
        cur.execute('''SELECT username FROM participants WHERE event_id=%s''', (row[0],))
        participant_rows = cur.fetchall()
        for participant_row in participant_rows:
            event["participants"].append(participant_row[0])

        events.append(event)

    cur.close()

    return events
