import unittest
from ..app import weber

class WeberTestCase(unittest.TestCase):
    def setUp(self):
        self.app = weber.app.test_client()

    def test_app(self):
        assert self.app

    def test_controller_page_load(self):
        result = self.app.get('/controller')
        assert "Brewer Controller" in result.data
        assert "Relays" in result.data
        assert "Temperatures" in result.data
