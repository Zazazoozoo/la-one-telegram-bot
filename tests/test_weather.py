import unittest
from app import create_app

class WeatherTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()


    def test_get_weather_success(self):
        city = 'London'
        response = self.client.get(f'/api/weather/{city}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('name', response.json())
        self.assertIn('temp', response.json())
        self.assertIn('description', response.json())

    def test_get_weather_invalid_city(self):
        city = 'not_a_real_city'
        response = self.client.get(f'/api/weather/{city}')
        self.assertEqual(response.status_code, 404)
        self.assertIn('message', response.json())
        self.assertEqual(response.json()['message'], 'city not found')

    def test_get_weather_missing_api_key(self):
        city = 'London'
        with app.test_request_context():
            app.config['OPENWEATHERMAP_API_KEY'] = None
            response = self.app.get(f'/api/weather/{city}')
            self.assertEqual(response.status_code, 500)
            self.assertIn('message', response.json())
            self.assertEqual(response.json()['message'], 'API key not set')

if __name__ == '__main__':
    unittest.main()
