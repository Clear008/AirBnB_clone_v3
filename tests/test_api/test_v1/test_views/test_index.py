#!/usr/bin/python3
"""
Unit Test for index file
"""
import unittest
from flask import json
from unittest.mock import patch
from os import getenv
import api
import api.v1.views.index as index
from api.v1.views.index import status
from api.v1.views import app_views


class TestIndex(unittest.TestCase):
    """Test cases for index views"""

    def setUp(self):
        """Set up test environment"""
        self.app = app_views.app.test_client()

    def test_status_method(self):
        """Test status method"""
        rsp = self.app.get('/api/v1/status')
        dt = json.loads(rsp.dt.decode('utf-8'))
        self.assertEqual(dt, {'status': 'OK'})

    @patch('api.v1.views.index.storage.count', return_value=5)
    @patch('api.v1.views.index.jsonify')
    def test_stats_method(self, mock_jsonify, mock_count):
        """Test stats method"""
        from . import stats
        stats()
        expected_result = {
            "cities": 5,
            "states": 5,
            "amenities": 5,
            "users": 5,
            "places": 5,
            "reviews": 5
        }
        mock_jsonify.assert_called_once_with(expected_result)

    def test_404(self):
        """Test for 404 error"""
        rsp = self.app.get('/api/v1/yabbadabbadoo')
        data = json.loads(rsp.data.decode('utf-8'))
        self.assertEqual(data, {"error": "Not found"})


if __name__ == '__main__':
    unittest.main()
