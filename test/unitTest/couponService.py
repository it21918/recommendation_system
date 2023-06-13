import unittest
import psycopg2
from unittest.mock import MagicMock

from services.couponService import DatabaseConnection, createCouponTable, insert_coupon, get_all_coupons


class DatabaseConnectionTestCase(unittest.TestCase):

    def test_get_instance(self):
        # Ensure that only one instance of DatabaseConnection is created
        instance1 = DatabaseConnection.get_instance()
        instance2 = DatabaseConnection.get_instance()

        self.assertIs(instance1, instance2)


class CouponDatabaseTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create a mock connection and cursor for testing
        cls.mock_conn = MagicMock(spec=psycopg2.extensions.connection)
        cls.mock_cursor = MagicMock(spec=psycopg2.extensions.cursor)

        # Patch the psycopg2.connect function to return the mock connection
        psycopg2.connect = MagicMock(return_value=cls.mock_conn)

    def setUp(self):
        # Reset the mock cursor for each test
        self.mock_cursor.reset_mock()

        # Set the mock cursor for the mock connection
        self.mock_conn.cursor.return_value = self.mock_cursor

    def test_createCouponTable(self):
        # Call the function
        createCouponTable()

        # Verify that the appropriate SQL commands were executed
        expected_commands = [
            "CREATE TABLE IF NOT EXISTS coupons (id SERIAL PRIMARY KEY, username varchar(50) NOT NULL REFERENCES users(username) ON DELETE CASCADE)",
            "CREATE TABLE IF NOT EXISTS selections (coupon_id integer NOT NULL REFERENCES coupons(id) ON DELETE CASCADE, event_id integer NOT NULL REFERENCES events(id) ON DELETE CASCADE, odds float NOT NULL, PRIMARY KEY (coupon_id, event_id));"
        ]
        self.assertEqual([c[0] for c in self.mock_cursor.execute.call_args_list], expected_commands)

    def test_insert_coupon(self):
        # Set up test data
        coupon = {
            "username": "test_user",
            "selections": [
                {"event_id": 1, "odds": 80},
                {"event_id": 2, "odds": 90}
            ]
        }

        # Call the function
        insert_coupon(coupon)

        # Verify that the appropriate SQL commands were executed
        expected_commands = [
            "INSERT INTO coupons (username) VALUES (%s) RETURNING id;",
            "INSERT INTO selections (coupon_id, event_id, odds) VALUES (%s, %s, %s);",
            "INSERT INTO selections (coupon_id, event_id, odds) VALUES (%s, %s, %s);",
        ]
        expected_params = [
            ("test_user",),
            (1, 1, 80),
            (1, 2, 90)
        ]
        self.assertEqual([c[0][0] for c in self.mock_cursor.execute.call_args_list], expected_commands)
        self.assertEqual([c[0][1] for c in self.mock_cursor.execute.call_args_list], expected_params)

    def test_get_all_coupons(self):
        # Set up mock data for the query results
        self.mock_cursor.fetchall.return_value = [
            (1, "user1"),
            (2, "user2"),
        ]
        self.mock_cursor.execute.side_effect = [
            None,
            [
                (1, 1, 80),
                (1, 2, 90)
            ],
            [
                (2, 3, 70),
                (2, 4, 85)
            ]
        ]

        # Call the function
        result = get_all_coupons()

        # Verify the result
        expected_result = [
            {
                "coupon_id": 1,
                "user_id": "user1",
                "selections": [
                    {"event_id": 1, "odds": 80},
                    {"event_id": 2, "odds": 90}
                ]
            },
            {
                "coupon_id": 2,
                "user_id": "user2",
                "selections": [
                    {"event_id": 3, "odds": 70},
                    {"event_id": 4, "odds": 85}
                ]
            }
        ]
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
