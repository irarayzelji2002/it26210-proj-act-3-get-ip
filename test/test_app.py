import unittest
from unittest.mock import patch
from app import get_ip_info, app
import json

class TestGetIPInfoFunction(unittest.TestCase):

    @patch('app.requests.get')
    def test_get_ip_info_valid_response(self, mock_get):
        """Test get_ip_info with a valid response."""
        mock_response = {
            "ip": "8.8.8.8",
            "country_name": "United States",
            "country_code": "US",
            "region": "California",
            "city": "Mountain View",
            "org": "Google LLC",
            "asn": "AS15169",
            "latitude": "37.4056",
            "longitude": "-122.0775",
            "version": "IPv4"
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        result = get_ip_info("8.8.8.8")
        self.assertEqual(result["ipv4"], "8.8.8.8")
        self.assertEqual(result["country"], "United States")
        self.assertEqual(result["city"], "Mountain View")

    @patch('app.requests.get')
    def test_get_ip_info_reserved_ip(self, mock_get):
        """Test get_ip_info with a reserved IP address."""
        mock_response = {
            "error": True,
            "reason": "Reserved IP Address",
            "ip": "192.168.0.1",
            "version": "IPv4"
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        result = get_ip_info("192.168.0.1")
        self.assertEqual(result["country"], "Reserved")
        self.assertIsNone(result["ipv4"])

    @patch('app.requests.get')
    def test_get_ip_info_api_error(self, mock_get):
        """Test get_ip_info when the API returns an error."""
        mock_get.return_value.status_code = 500
        mock_get.return_value.json.side_effect = ValueError

        result = get_ip_info("8.8.8.8")
        self.assertEqual(result["error"], "Unable to fetch IP information.")

class TestFlaskRoutes(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.requests.get')
    def test_ip_info_route(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "ip": "8.8.8.8",
            "version": "IPv4",
            "country_name": "United States",
            "country_code": "US",
            "region": "California",
            "city": "Mountain View",
            "org": "Google LLC",
            "asn": "AS15169",
            "latitude": 37.386,
            "longitude": -122.0838,
        }

        response = self.app.get('/get-ip-info?ip=8.8.8.8')
        self.assertEqual(response.status_code, 200)

        response_data = json.loads(response.data)
        self.assertEqual(response_data['ipv4'], "8.8.8.8")

    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertIn('/get-ip-page', response.headers['Location'])

    def test_show_get_ip_page(self):
        response = self.app.get('/get-ip-page')
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
