from django.test import TestCase
from rest_framework.test import APIClient

class VayuLensAppTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_root_redirect(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/dashboard/')

    def test_pages(self):
        pages = ['/dashboard/', '/monitoring/', '/forecast/', '/historical/', '/stations/', '/model-insights/', '/about/']
        for page in pages:
            res = self.client.get(page)
            self.assertEqual(res.status_code, 200, f"Page {page} failed with status {res.status_code}")

    def test_api_health(self):
        response = self.client.get('/api/health/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['success'])

    def test_api_current_station(self):
        response = self.client.get('/api/air-quality/current/?station=jayanagar')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['data']['name'], 'Jayanagar 4th Block')

    def test_api_dashboard_station(self):
        response = self.client.get('/api/dashboard/live/?station=peenya')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['data']['selected_station']['id'], 'peenya')

    def test_api_prediction(self):
        response = self.client.get('/api/prediction/?station=cubbon-park')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['success'])

    def test_api_historical(self):
        response = self.client.get('/api/historical/?range=7d')
        self.assertEqual(response.status_code, 200)

    def test_api_stations(self):
        response = self.client.get('/api/stations/')
        self.assertEqual(response.status_code, 200)

    def test_api_model_insights(self):
        response = self.client.get('/api/model/insights/')
        self.assertEqual(response.status_code, 200)
