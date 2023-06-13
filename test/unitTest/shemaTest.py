import unittest

from services.validator import validate_coupon_schema, validate_event_schema, validate_user_schema


class TestSchema(unittest.TestCase):

    def setUp(self):
        self.valid_users = [
            {
                "username": "user123",
                "birth_year": 1990,
                "country": "USA",
                "currency": "USD",
                "registration_date": "2022-01-01T00:00:00Z",
                "friends": ["user456", "user789"]
            },
            {
                "username": "user456",
                "birth_year": 1995,
                "country": "Canada",
                "currency": "CAD",
                "registration_date": "2022-01-01T00:00"
            }
        ]

        self.valid_user = {
            "username": "user123",
            "birth_year": 1990,
            "country": "USA",
            "currency": "USD",
            "registration_date": "2022-01-01T00:00:00Z",
            "friends": ["user456", "user789"]
        }

        self.invalid_user = {
            "username": "user123",
            "birth_year": "1990",
            "country": "USA",
            "currency": "USD",
            "registration_date": "2022-01-01T00:00:00Z",
            "friends": ["user456", "user789"]
        }

        self.valid_coupon = {
            "selections": [
                {
                    "event_id": 1234,
                    "odds": 1.5
                },
                {
                    "event_id": 5678,
                    "odds": 2.0
                }
            ],
            "username": "user123"
        }

        self.invalid_coupon = {
            "selections": [
                {
                    "event_id": "1234",
                    "odds": 1.5
                },
                {
                    "event_id": 5678,
                    "odds": "2.0"
                }
            ],
            "username": "user123"
        }

        self.valid_event = {
            "begin_timestamp": "2022-05-01T12:00:00Z",
            "country": "USA",
            "end_timestamp": "2022-05-01T14:00:00Z",
            "league": "NFL",
            "participants": ["New England Patriots", "Dallas Cowboys"],
            "sport": "Football"
        }

        self.invalid_event = {
            "begin_timestamp": "2022-05-01 12:00:00",
            "country": "USA",
            "end_timestamp": "2022-05-01T14:00:00Z",
            "league": "NFL",
            "participants": ["New England Patriots", "Dallas Cowboys"]
        }

    def test_coupon_schema_validation(self):
        assert validate_coupon_schema(self.valid_coupon) == (True, "Coupon schema is valid.")
        assert validate_coupon_schema(self.invalid_coupon) == (False, "'1234' is not of type 'integer'")

    def test_event_schema_validation(self):
        assert validate_event_schema(self.valid_event) == (True, "Event schema is valid.")
        assert validate_event_schema(self.invalid_event) == (False, "'sport' is a required property")

    def test_user_schema_validation(self):
        assert validate_user_schema(self.valid_user) == (True, "User schema is valid.")
        assert validate_user_schema(self.invalid_user) == (False, "'1990' is not of type 'integer'")
