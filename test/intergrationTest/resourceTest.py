import json
import unittest
from unittest.mock import patch
from app import app


class TestCreateUser(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.user_data = {
            "username": "testUser",
            "birth_year": 1995,
            "country": "USA",
            "currency": "USD",
            "friends": []
        }

        self.user_data_failure = {
            'birth_year': 1995,
            'country': 'USA',
            'currency': 'USD',
            'friends': []
        }

        self.event_data = {
            'begin_timestamp': '2022-04-07 15:30:00+0000',
            'country': 'USA',
            'end_timestamp': '2022-04-07 17:30:00+0000',
            'event_id': 'abc123',
            'league': 'NFL',
            'participants': ['team1', 'team2'],
            'sport': 'Football'
        }

        self.event_data_failure = {
            'begin_timestamp': '2022-04-07 15:30:00+0000',
            'end_timestamp': '2022-04-07 17:30:00+0000',
            'league': 'NFL',
            'participants': ['team1', 'team2'],
            'sport': 'Football',
            'country': 'USA'
        }

    @patch('services.userService.insert_user')
    @patch('schema.validate_user_schema')
    def test_create_user(self, insert_user_mock, validate_user_schema_mock):
        response = self.app.post('/create_user', json=self.user_data)
        # insert_user_mock.assert_called_with(user=self.user_data)
        # validate_user_schema_mock.assert_called_with(self.user_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['message'], 'User created successfully.')

    def test_create_user_missing_data(self):
        response = self.app.post('/create_user', json=self.user_data_failure)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data)['error']['user_id'][0], 'Missing data for required field.')

    def test_create_event(self):
        response = self.app.post('/create_event', json=self.event_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['message'], 'Event created successfully.')

    def test_create_event_missing_data(self):
        response = self.app.post('/create_event', json=self.event_data_failure)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data)['error']['event_id'][0], 'Missing data for required field.')

    def test_get_recommendations_based_on_similarity(self):
        response = self.app.get('/recommendations_similarity/1')
        assert response.status_code == 200
        assert 'recommendation based on similarity' in response.json

    def test_get_recommendations_based_on_friends(self):
        response = self.app.get('/recommendations_friends/1')
        assert response.status_code == 200
        assert 'recommendation based on your friends:' in response.json

    def test_get_coupons(self):
        # test getting all coupons
        response = self.app.get('/get_coupons')
        assert response.status_code == 200