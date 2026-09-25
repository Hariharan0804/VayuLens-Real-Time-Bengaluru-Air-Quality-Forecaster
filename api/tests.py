from django.test import TestCase
from rest_framework.test import APIClient

class VayuLensAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_health(self):
        response = self.client.get('/api/health/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['success'])

    def test_current(self):
        response = self.client.get('/api/air-quality/current/')
        self.assertEqual(response.status_code, 200)

    def test_prediction(self):
        response = self.client.get('/api/prediction/')
        self.assertEqual(response.status_code, 200)

    def test_dashboard(self):
        response = self.client.get('/api/dashboard/live/')
        self.assertEqual(response.status_code, 200)

    def test_historical(self):
        response = self.client.get('/api/historical/?range=7d')
        self.assertEqual(response.status_code, 200)

    def test_stations(self):
        response = self.client.get('/api/stations/')
        self.assertEqual(response.status_code, 200)

    def test_model_insights(self):
        response = self.client.get('/api/model/insights/')
        self.assertEqual(response.status_code, 200)
