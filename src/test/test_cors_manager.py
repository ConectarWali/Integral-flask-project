import unittest
from unittest.mock import patch
from flask import Flask
from src.config.cors_config import CORS_manager

class TestCORSManager(unittest.TestCase):
    def setUp(self):
        """Set up test cases with a mock Flask app"""
        self.app = Flask(__name__)
        self.cors_manager = CORS_manager(self.app)

    def test_create_config_without_name(self):
        """Test creating config without name raises ValueError"""
        with self.assertRaises(ValueError):
            self.cors_manager.create_config()

    def test_create_config_with_name(self):
        """Test creating config with name"""
        self.cors_manager.create_config(
            name="test",
            origins=["http://localhost:3000"],
            methods=["GET", "POST"]
        )
        self.assertIn("test", self.cors_manager.configs)

    def test_get_endpoints(self):
        """Test getting endpoints for a blueprint"""
        # Create a test blueprint
        @self.app.route("/test")
        def test_route():
            return "test"

        endpoints = self.cors_manager._get_endpoints("test")
        self.assertIsInstance(endpoints, list)

    @patch('flask_cors.CORS')
    def test_apply_cors(self, mock_cors):
        """Test applying CORS configurations"""
        self.cors_manager.create_config(
            name="test",
            origins=["http://localhost:3000"]
        )
        self.cors_manager._apply_cors()
        mock_cors.assert_called_once()

    def test_headers_added_to_response(self):
        """Test CORS headers are added to response"""
        self.cors_manager.create_config(
            name="test",
            origins=["http://localhost:3000"],
            headers=["X-Test-Header"]
        )

        with self.app.test_client() as client:
            response = client.get('/')
            self.assertIn('Access-Control-Allow-Origin', response.headers)

if __name__ == '__main__':
    unittest.main()