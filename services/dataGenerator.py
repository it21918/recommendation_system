import random
import string
import datetime

from userService import get_all_users
from eventService import get_all_events

def generate_user():
    """Generates a random user based on the UserSchema."""
    try:
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
    except:
        print("error trying again")
        generate_user()


def generate_event():
    """Generates a random event based on the EventSchema."""
    try:
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
    except:
        print("error trying again")
        generate_event()


def generate_coupon(num_events=3):
    users = get_all_users()
    if len(users) == 0:
        print(users)
        return -1
    events = get_all_events()

    user = random.choice(users)
    selected_events = random.sample(events, num_events)  # Select multiple random events

    registration_date = user["registration_date"]

    coupon = {
        "username": user["username"],
        "selections": [],
        "created_date": (datetime.datetime.utcnow() + datetime.timedelta(days=random.randint(1, 30))).isoformat()
    }

    for event in selected_events:
        event_end_timestamp = event["end_timestamp"]

        score = 0
        if event['country'] == user['country']:
            score += 1
        if event['begin_timestamp'] > user['registration_date']:
            score += 1
        if event['end_timestamp'] > user['registration_date']:
            score += 1

        if registration_date < event_end_timestamp:
            selection = {
                "event_id": event["id"],
                "odds": score / 3 * 100
            }
            coupon["selections"].append(selection)

    if len(coupon["selections"]) > 0:
        return coupon
    else:
        print("error trying again")
        return generate_coupon()

