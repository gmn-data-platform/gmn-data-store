"""Tests for the setup_database module"""
import unittest
from unittest import mock

import sqlalchemy
from sqlalchemy.orm import sessionmaker

import gmn_data_store.setup_database


class TestSetupDatabase(unittest.TestCase):
    """Tests for the setup_database module."""

    def setUp(self) -> None:
        self.test_showers = {
            "test1": {"id": 1, "code": "aaa", "name": "bbb"},
            "test2": {"id": 2, "code": "ccc", "name": "ddd"},
            "test3": {"id": 3, "code": "eee", "name": "fff"},
        }

    @mock.patch("gmn_data_store.controller.get_session")
    @mock.patch("gmn_data_store.setup_database.get_engine")
    @mock.patch("gmn_data_store.setup_database.get_iau_showers")
    def test_setup_database_showers(
        self,
        mock_showers: mock.Mock,
        mock_engine: mock.Mock,
        mock_session_maker: mock.Mock,
    ) -> None:
        """
        Test: That setup_database() creates the correct showers.
        When: setup_database() is called.
        """
        mock_showers.return_value = self.test_showers

        engine = sqlalchemy.create_engine("sqlite://", echo=True)
        mock_engine.return_value = engine
        mock_session_maker.return_value = sessionmaker(bind=engine)()

        gmn_data_store.setup_database.setup_database()

        self.assertEqual(
            [tuple(i.values()) for i in self.test_showers.values()],
            [i[:3] for i in engine.execute("SELECT * FROM iau_shower").fetchall()],
        )
