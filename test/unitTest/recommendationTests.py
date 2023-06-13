import unittest
from unittest.mock import patch

from recommendation import recommend_events_based_on_similarity, popularEvents, recommend_coupon_from_popular_coupons
from recommendation import recommend_coupons_based_on_friends


class TestRecommendationMethods(unittest.TestCase):
    def setUp(self):
        self.all_events = [
            {'id': 1, 'country': 'USA', 'begin_timestamp': '2023-05-01T00:00:00Z',
             'end_timestamp': '2023-05-03T00:00:00Z'},
            {'id': 2, 'country': 'Canada', 'begin_timestamp': '2023-05-01T00:00:00Z',
             'end_timestamp': '2023-05-03T00:00:00Z'},
            {'id': 3, 'country': 'USA', 'begin_timestamp': '2023-05-05T00:00:00Z',
             'end_timestamp': '2023-05-07T00:00:00Z'},
            {'id': 4, 'country': 'Canada', 'begin_timestamp': '2023-05-05T00:00:00Z',
             'end_timestamp': '2023-05-07T00:00:00Z'},
        ]
        self.user = {
            "username": "user123",
            "birth_year": 1990,
            "country": "USA",
            "currency": "USD",
            "registration_date": "2022-01-01T00:00:00Z",
            "friends": ["user456", "user789"]
        }

        self.friend_coupons = [
            [
                {'selections': [{'event_id': 1, 'odds': 2}, {'event_id': 2, 'odds': 3}]},
                {'selections': [{'event_id': 3, 'odds': 4}, {'event_id': 4, 'odds': 5}]},
            ],
            [
                {'selections': [{'event_id': 1, 'odds': 6}, {'event_id': 2, 'odds': 7}]},
                {'selections': [{'event_id': 3, 'odds': 8}, {'event_id': 4, 'odds': 9}]},
            ],
        ]

        self.user = {
            "username": "user123",
            "birth_year": 1990,
            "country": "USA",
            "currency": "USD",
            "registration_date": "2022-01-01T00:00:00Z",
            "friends": ["user456", "user789"]
        }

    @patch('recommendation.recommend_events_based_on_similarity')
    def test_recommend_events_based_on_similarity(self, mock_recommend_events):
        # Test the function
        recommended_coupon = recommend_events_based_on_similarity(self.all_events, self.user, limit=2)

        # Check the result
        self.assertEqual(len(recommended_coupon['selections']), 2)
        self.assertEqual(recommended_coupon['username'], 'user123')
        self.assertEqual(recommended_coupon['selections'][0]['event_id'], 1)
        self.assertEqual(recommended_coupon['selections'][0]['odds'], 100)
        self.assertEqual(recommended_coupon['selections'][1]['event_id'], 3)
        self.assertEqual(recommended_coupon['selections'][1]['odds'], 100)
        # mock_recommend_events.assert_called_once()

    def test_recommend_coupons_based_on_friends(self):
        # Test the function
        recommended_coupon = recommend_coupons_based_on_friends(self.friend_coupons, self.user)

        # Check the result
        self.assertEqual(recommended_coupon['username'], 'user123')
        self.assertEqual(len(recommended_coupon['selections']), 8)
        self.assertIn({'event_id': 1, 'odds': 2}, recommended_coupon['selections'])
        self.assertIn({'event_id': 2, 'odds': 3}, recommended_coupon['selections'])
        self.assertIn({'event_id': 3, 'odds': 4}, recommended_coupon['selections'])
        self.assertIn({'event_id': 4, 'odds': 5}, recommended_coupon['selections'])
        self.assertIn({'event_id': 1, 'odds': 6}, recommended_coupon['selections'])
        self.assertIn({'event_id': 2, 'odds': 7}, recommended_coupon['selections'])
        self.assertIn({'event_id': 3, 'odds': 8}, recommended_coupon['selections'])
        self.assertIn({'event_id': 4, 'odds': 9}, recommended_coupon['selections'])

    def test_popularEvents(self):
        coupons = [
            {
                "selections": [
                    {"event_id": 1, "odds": 80},
                    {"event_id": 2, "odds": 60},
                    {"event_id": 3, "odds": 70}
                ]
            },
            {
                "selections": [
                    {"event_id": 2, "odds": 90},
                    {"event_id": 1, "odds": 75},
                    {"event_id": 5, "odds": 85}
                ]
            },
            {
                "selections": [
                    {"event_id": 1, "odds": 95},
                ]
            }
        ]

        popular_events = popularEvents(coupons)

        expected_result = [1,2,3,5]
        self.assertEqual(popular_events, expected_result)

    def test_recommend_coupon_from_popular_coupons(self):
        events = [2, 1, 3, 5, 4]
        limit = 3
        user = {"username": "test_user"}

        recommended_coupon = recommend_coupon_from_popular_coupons(events, limit, user)

        expected_result = {
            "selections": [2, 1, 3],
            "username": "test_user"
        }
        self.assertEqual(recommended_coupon, expected_result)


if __name__ == '__main__':
    unittest.main()
