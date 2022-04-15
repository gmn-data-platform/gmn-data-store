"""Tests for the setup_database module"""
import sys
import unittest
from unittest import mock


class TestSetupDatabase(unittest.TestCase):
    """Tests for the setup_database module."""

    def setUp(self) -> None:
        """Setup tests."""
        try:
            del sys.modules["gmn_data_store"]
        except KeyError:  # pragma: no cover
            pass

    @mock.patch("gmn_data_store._DB_CONNECTION_URI", "sqlite://")
    @mock.patch("gmn_data_store.setup_database.get_iau_showers")
    def test_setup_database_showers(self, mock_showers: mock.Mock) -> None:
        """
        Test: That setup_database() creates the correct showers.
        When: setup_database() is called.
        """
        import gmn_data_store.setup_database

        test_showers = {
            "test1": {"id": 1, "code": "aaa", "name": "bbb"},
            "test2": {"id": 2, "code": "ccc", "name": "ddd"},
            "test3": {"id": 3, "code": "eee", "name": "fff"},
        }
        mock_showers.return_value = test_showers
        engine = gmn_data_store.setup_database.setup_database()

        self.assertEqual(
            [tuple(i.values()) for i in test_showers.values()],
            [i[:3] for i in engine.execute("SELECT * FROM iau_shower").fetchall()],
        )
