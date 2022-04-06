"""Tests for the models module"""
import sys
import unittest
from unittest import mock

from sqlalchemy import Column
from sqlalchemy import String


class TestModels(unittest.TestCase):
    """Tests for the models module."""

    def tearDown(self):
        """
        Tear down the test.
        """
        try:
            del sys.modules["gmn_data_store.setup_database"]
            del sys.modules["gmn_data_store.models"]
            del sys.modules["gmn_data_store.controller"]
        except KeyError:
            pass

    @mock.patch("gmn_data_store._DB_CONNECTION_URI", "sqlite://")
    def test_add_column_pre_existing_columns_dont_alter_db(self) -> None:
        """
        Test: That _add_column() handles adding columns that already exist.
        When: _add_column() is called with alter_table=False.
        """
        from gmn_data_store.setup_database import setup_database
        from gmn_data_store.models import _add_column, Meteor

        engine = setup_database()

        expected_columns = Meteor.__table__.columns.keys() + ["test"]
        expected_database_columns = [
            i[1] for i in engine.execute("PRAGMA table_info(meteor)").fetchall()
        ]

        # Don't alter database table
        col1 = Column("test", String)
        col2 = col1.copy()
        _add_column(engine, "meteor", Meteor, col1, False)
        _add_column(engine, "meteor", Meteor, col2, False)

        self.assertEqual(expected_columns, list(Meteor.__table__.columns.keys()))
        self.assertEqual(
            expected_database_columns,
            [i[1] for i in engine.execute("PRAGMA table_info(meteor)").fetchall()],
        )

    @mock.patch("gmn_data_store._DB_CONNECTION_URI", "sqlite://")
    def test_add_column_pre_existing_columns_alter_db(self) -> None:
        """
        Test: That _add_column() handles adding columns that already exist.
        When: _add_column() is called with alter_table=True.
        """
        from gmn_data_store.setup_database import setup_database
        from gmn_data_store.models import _add_column, Meteor

        engine = setup_database()

        expected_columns = Meteor.__table__.columns.keys() + ["test"]
        expected_database_columns = [
            i[1] for i in engine.execute("PRAGMA table_info(meteor)").fetchall()
        ] + ["test"]

        # Don't alter database table
        col = Column("test", String)
        _add_column(engine, "meteor", Meteor, col, True)
        _add_column(engine, "meteor", Meteor, col, True)

        self.assertEqual(expected_columns, list(Meteor.__table__.columns.keys()))
        self.assertEqual(
            expected_database_columns,
            [i[1] for i in engine.execute("PRAGMA table_info(meteor)").fetchall()],
        )
