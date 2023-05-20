import random
import string
import datetime
from userService import get_all_users
from eventService import get_all_events

def generate_user():
    """Generates a random user based on the UserSchema."""

    username = ''.join(random.choices(string.ascii_letters, k=10))
    birth_year = random.randint(1950, 2020)
    country = random.choice(["USA", "Canada", "Mexico", "UK", "Germany", "France", "Japan", "China", "India"])
    currency = random.choice(["USD", "CAD", "MXN", "GBP", "EUR", "JPY", "CNY", "INR"])
    registration_date = datetime.datetime.utcnow().isoformat()
    users = get_all_users()

    friend_usernames = random.sample([user['username'] for user in users], k=random.randint(0, len(users)))
    friends = friend_usernames

    return {
        "username": username,
        "birth_year": birth_year,
        "country": country,
        "currency": currency,
        "registration_date": registration_date,
        "friends": friends
    }


def generate_event():
    """Generates a random event based on the EventSchema."""

    begin_timestamp = (datetime.datetime.utcnow() + datetime.timedelta(days=random.randint(1, 30))).isoformat()
    end_timestamp = (datetime.datetime.utcnow() + datetime.timedelta(days=random.randint(31, 60))).isoformat()
    country = random.choice(["USA", "Canada", "Mexico", "UK", "Germany", "France", "Japan", "China", "India"])
    league = random.choice(
        ["NFL", "NBA", "MLB", "NHL", "Premier League", "Bundesliga", "Ligue 1", "Serie A", "La Liga"])
    sport = random.choice(["Football", "Basketball", "Baseball", "Hockey", "Soccer", "Tennis", "Golf"])
    participants = [f"team_{random.randint(1, 20)}" for _ in range(random.randint(2, 5))]
    return {
        "begin_timestamp": begin_timestamp,
        "end_timestamp": end_timestamp,
        "country": country,
        "league": league,
        "sport": sport,
        "participants": participants
    }

def generate_coupon():
    users = get_all_users()
    events = get_all_events()

    user = random.choice(users)
    event = random.choice(events)

    registration_date = user["registration_date"]
    event_end_timestamp = event["end_timestamp"]

    score = 0
    if event['country'] == user['country']:
        score += 1
    if abs((event['begin_timestamp'] > user['registration_date'])):
        score += 1
    if abs((event['end_timestamp'] > user['registration_date'])):
        score += 1

    if registration_date < event_end_timestamp:
        coupon = {
            "username": user["username"],
            "selections": [
                {
                    "event_id": event["id"],
                    "odds": score / 3 * 100
                }
            ]
        }
        return coupon
    else:
        raise Exception("Invalid coupon: User registration date is after the event end timestamp")
