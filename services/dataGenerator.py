import random
import string
import datetime
from userService import get_all_users


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
