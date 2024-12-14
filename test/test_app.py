import unittest
from unittest.mock import patch
from app import get_ip_info, get_ip_reputation, app
import json

class TestGetIPInfoFunction(unittest.TestCase):

    @patch('app.requests.get')
    def test_get_ip_info_valid_response(self, mock_get):
        """Test get_ip_info with a valid response."""
        mock_response = {
            "ip": "8.8.8.8",
            "country": "US",
            "region": "California",
            "city": "Mountain View",
            "org": "AS15169 Google LLC",
            "asn": "AS15169",
            "loc": "37.386,-122.0838",
            "postal": "94043"
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        result = get_ip_info("8.8.8.8")
        self.assertEqual(result["ipv4"], "8.8.8.8")
        self.assertEqual(result["country"], "US")
        self.assertEqual(result["region"], "California")
        self.assertEqual(result["city"], "Mountain View")
        self.assertEqual(result["asn"], "AS15169")
        self.assertEqual(result["latitude"], "37.386")
        self.assertEqual(result["longitude"], "-122.0838")

    @patch('app.requests.get')
    def test_get_ip_info_bogon_ip(self, mock_get):
        """Test get_ip_info with a bogon IP address."""
        mock_response = {
            "ip": "192.168.60.61",
            "bogon": True
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        result = get_ip_info("192.168.60.61")
        self.assertEqual(result["ipv4"], "192.168.60.61")
        self.assertIsNone(result["ipv6"])
        self.assertIsNone(result["country"])
        self.assertIsNone(result["region"])
        self.assertIsNone(result["city"])
        self.assertEqual(result["note"], "Minimal information returned for this IP address.")

    @patch('app.requests.get')
    def test_get_ip_info_no_ip_info(self, mock_get):
        """Test get_ip_info when no information is available for IP."""
        mock_response = {
            "ip": "2001:db8:3333:4444:5555:6666:7777:8888",
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        result = get_ip_info("2001:db8:3333:4444:5555:6666:7777:8888")
        self.assertIsNone(result["ipv4"])
        self.assertEqual(result["ipv6"], "2001:db8:3333:4444:5555:6666:7777:8888")

    @patch('app.requests.get')
    def test_get_ip_info_api_error(self, mock_get):
        """Test get_ip_info when the API returns an error."""
        mock_get.return_value.status_code = 500
        mock_get.return_value.json.side_effect = ValueError

        result = get_ip_info("8.8.8.8")
        self.assertEqual(result["error"], "Unable to fetch IP information.")


    @patch('app.requests.get')
    def test_get_ip_reputation_valid_response(self, mock_get):
        """Test get_ip_reputation with a valid response."""
        mock_response = {
            "success": True,
            "fraud_score": 0,
            "country_code": "US",
            "region": "Colorado",
            "city": "Denver",
            "ISP": "Cloudflare",
            "ASN": 13335,
            "organization": "Cloudflare",
            "is_crawler": False,
            "timezone": "America/Denver",
            "mobile": False,
            "host": "one.one.one.one",
            "proxy": False,
            "vpn": False,
            "tor": False,
            "active_vpn": False,
            "active_tor": False,
            "recent_abuse": False,
            "bot_status": True,
            "connection_type": "Premium required.",
            "abuse_velocity": "Premium required.",
            "zip_code": "N/A",
            "latitude": 39.75,
            "longitude": -105
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        result = get_ip_reputation("8.8.8.8")
        self.assertEqual(result["fraud_score"], 0)
        self.assertEqual(result["bot_status"], True)
        self.assertEqual(result["connection_type"], "Premium required.")

    @patch('app.requests.get')
    def test_get_ip_reputation_api_error(self, mock_get):
        """Test get_ip_reputation when the API returns an error."""
        mock_response = {
            "success": False, 
            "message": ""
        }
        mock_get.return_value.json.return_value = mock_response

        result = get_ip_reputation("")
        self.assertEqual(result["error"], "IP address is required")

class TestFlaskRoutes(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.requests.get')
    def test_ip_info_route(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "ip": "8.8.8.8",
            "country": "US",
            "region": "California",
            "city": "Mountain View",
            "org": "AS15169 Google LLC",
            "asn": "AS15169",
            "loc": "37.386,-122.0838",
            "postal": "94043"
        }

        response = self.app.get('/get-ip-info?ip=8.8.8.8')
        self.assertEqual(response.status_code, 200)

        response_data = json.loads(response.data)
        self.assertEqual(response_data['ip_info']['ipv4'], "8.8.8.8")

    @patch('app.requests.get')
    def test_ip_info_route_bogon(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "ip": "192.168.60.61",
            "bogon": True
        }

        response = self.app.get('/get-ip-info?ip=192.168.60.61')
        self.assertEqual(response.status_code, 200)

        response_data = json.loads(response.data)
        self.assertEqual(response_data['ip_info']['ipv4'], "192.168.60.61")

    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertIn('/get-ip-page', response.headers['Location'])

    def test_show_get_ip_page(self):
        response = self.app.get('/get-ip-page')
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
