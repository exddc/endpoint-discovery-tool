import unittest
from tests import simple_http_server
import threading
from src import scraper

class TestScraperWithServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up the mock API server before any tests run."""
        cls.server_thread = threading.Thread(target=simple_http_server.run, args=(['/api', '/v9/dashboard']), daemon=True, name='MockServer')
        cls.server_thread.start()
        print("Mock HTTP server started for testing...")

    @classmethod
    def tearDownClass(cls):
        """Shut down the mock HTTP server after all tests run."""
        simple_http_server.stop()
        cls.server_thread.join()
        print("Mock HTTP server shutdown.")

    def test_read_endpoints_config(self):
        """Test that the configuration file is read correctly."""
        config = scraper.read_endpoints_config()
        self.assertIsInstance(config, dict)
        self.assertIn('snippets', config)
        self.assertIn('full', config)

if __name__ == '__main__':
    unittest.main()
