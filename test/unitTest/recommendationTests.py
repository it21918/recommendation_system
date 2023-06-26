import unittest
from unittest.mock import patch
from recommendation import createGraph, haveSimilarSelections, findSimilarCoupons
from recommendation import recommend_events_based_on_similarity, findSimilarCoupons
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

    def test_createGraph(self):
        coupons = [
            {
                "id": 1,
                "selections": [
                    {"event_id": 1, "odds": 2.0},
                    {"event_id": 2, "odds": 1.5}
                ]
            },
            {
                "id": 2,
                "selections": [
                    {"event_id": 2, "odds": 1.5},
                    {"event_id": 3, "odds": 3.0}
                ]
            },
            {
                "id": 3,
                "selections": [
                    {"event_id": 1, "odds": 2.0},
                    {"event_id": 3, "odds": 3.0}
                ]
            }
        ]

        G = createGraph(coupons)

        # Check if the graph has the correct number of nodes and edges
        self.assertEqual(len(G.nodes), 3)
        self.assertEqual(len(G.edges), 0)

        # Check if the node attributes are correctly set
        self.assertDictEqual(G.nodes[1], {"selections": [{"event_id": 1, "odds": 2.0}, {"event_id": 2, "odds": 1.5}]})
        self.assertDictEqual(G.nodes[2], {"selections": [{"event_id": 2, "odds": 1.5}, {"event_id": 3, "odds": 3.0}]})
        self.assertDictEqual(G.nodes[3], {"selections": [{"event_id": 1, "odds": 2.0}, {"event_id": 3, "odds": 3.0}]})

    def test_haveSimilarSelections(self):
        selections1 = [
            {"event_id": 1, "odds": 2.0},
            {"event_id": 2, "odds": 1.5}
        ]
        selections2 = [
            {"event_id": 2, "odds": 1.5},
            {"event_id": 3, "odds": 3.0}
        ]
        threshold = 0.5

        # Check if the selections are similar
        self.assertTrue(haveSimilarSelections(selections1, selections2, threshold))

        selections3 = [
            {"event_id": 5, "odds": 2.0},
            {"event_id": 3, "odds": 3.0}
        ]

        # Check if the selections are not similar
        self.assertFalse(haveSimilarSelections(selections1, selections3, threshold))

    def test_findSimilarCoupons(self):
        coupons = [
            {
                "id": 1,
                "selections": [
                    {"event_id": 1, "odds": 2.0},
                    {"event_id": 2, "odds": 1.5},
                    {"event_id": 3, "odds": 3.0}
                ]
            },
            {
                "id": 2,
                "selections": [
                    {"event_id": 1, "odds": 2.0},
                    {"event_id": 2, "odds": 1.5},
                    {"event_id": 3, "odds": 3.0}
                ]
            },
            {
                "id": 3,
                "selections": [
                    {"event_id": 1, "odds": 2.0},
                    {"event_id": 5, "odds": 3.0}
                ]
            }
        ]

        coupon_id = 1
        threshold = 0.5
        limit = 3

        similar_coupons = findSimilarCoupons(coupons, coupon_id, threshold, limit)

        # Check if the function returns the correct list of similar coupon IDs
        self.assertEqual(similar_coupons, [2])


if __name__ == '__main__':
    unittest.main()
