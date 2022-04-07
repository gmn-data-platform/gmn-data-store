"""Tests for the controller module."""
import datetime
import unittest
from unittest import mock

import gmn_python_api  # type: ignore
import sqlalchemy  # type: ignore
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import sessionmaker  # type: ignore

import gmn_data_store.controller
import gmn_data_store.models
import gmn_data_store.setup_database


class Test(gmn_data_store.models._Base):  # type: ignore
    """Tests for the controller module."""

    __tablename__ = "test"

    id = Column(Integer, primary_key=True)
    name = Column(String)


class TestController(unittest.TestCase):
    """Tests for the controller module."""

    @mock.patch("gmn_data_store.controller.get_session")
    @mock.patch("gmn_data_store.setup_database.get_engine")
    def test_create_row(
        self, mock_engine: mock.Mock, mock_session_maker: mock.Mock
    ) -> None:
        """
        Test: That create_row() creates the correct row.
        When: create_row() is called.
        """
        engine = sqlalchemy.create_engine("sqlite://", echo=True)
        mock_engine.return_value = engine
        mock_session_maker.return_value = sessionmaker(bind=engine)()

        expected_row = {"id": 1, "name": "test"}
        engine.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)")

        gmn_data_store.controller.create_row(Test, expected_row)

        self.assertEqual(
            list(expected_row.values()),
            list(engine.execute("SELECT * FROM test").fetchall()[0]),
        )

    @mock.patch("gmn_data_store.controller.get_session")
    @mock.patch("gmn_data_store.get_engine")
    @mock.patch("gmn_data_store.setup_database.get_engine")
    def test_create_row_already_exists(
        self,
        mock_engine: mock.Mock,
        mock_engine2: mock.Mock,
        mock_session_maker: mock.Mock,
    ) -> None:
        """
        Test: That create_row() doesn't create a new row if the id already exists.
        When: create_row() is called.
        """
        engine = sqlalchemy.create_engine("sqlite://", echo=True)
        mock_engine.return_value = engine
        mock_engine2.return_value = engine
        mock_session_maker.return_value = sessionmaker(bind=engine)()

        expected_row = {"id": 1, "name": "test"}
        engine.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)")
        engine.execute("INSERT INTO test VALUES (1, 'test')")

        gmn_data_store.controller.create_row(Test, expected_row)

        self.assertEqual(
            list(expected_row.values()),
            list(engine.execute("SELECT * FROM test").fetchall()[0]),
        )

    @mock.patch("gmn_data_store._DB_CONNECTION_URI", "sqlite://")
    def test_insert_trajectory_summary(self) -> None:
        """
        Test: That insert_trajectory_summary() creates the correct row in the Meteor
         table from a trajectory summary json.
        When: insert_trajectory_summary() is called.
        """
        data_frame = gmn_python_api.read_trajectory_summary_as_dataframe(
            gmn_python_api.trajectory_summary_schema._MODEL_TRAJECTORY_SUMMARY_FILE_PATH,
            avro_compatible=True,
        )
        schema = gmn_python_api.get_trajectory_summary_avro_schema()
        timestamp_fields = [
            item["name"]
            for item in schema["fields"]
            if item["type"]
            == ["null", {"type": "long", "logicalType": "timestamp-micros"}]
        ]

        engine = gmn_data_store.setup_database.setup_database()

        expected_row = data_frame.iloc[0].to_dict()
        gmn_data_store.controller.insert_trajectory_summary(expected_row, engine)

        # Extract fields that should be in the Meteor table
        expected_row_db = {}

        for k in set(gmn_data_store.models.Meteor.__table__.columns.keys()) - set(
            gmn_data_store.models._FIELDS_IN_METEOR_TABLE_NOT_TRAJECTORY_SUMMARY
        ):
            value = expected_row[k]
            if value in (True, False):
                value = int(value)
            elif k in timestamp_fields:
                value = datetime.datetime.fromtimestamp(value / 1e6).strftime(
                    "%Y-%m-%d %H:%M:%S.%f"
                )
            expected_row_db[k] = value

        # Test if the trajectory summary data is in the meteor table
        self.assertTrue(
            set(expected_row_db.values()).issubset(
                set(engine.execute("SELECT * FROM meteor").fetchall()[0])
            )
        )

        # Test if the iau_shower table contains the stations from the trajectory summary
        self.assertEqual(
            {x[0] for x in engine.execute("SELECT code FROM station").fetchall()},
            set(expected_row["participating_stations"]),
        )

        # Test if the participating_station table contains the showers in the trajectory
        # summary
        participating_stations = engine.execute(
            "SELECT meteor_id, station_id FROM participating_station"
        ).fetchall()
        for row in participating_stations:
            self.assertEqual(expected_row["unique_trajectory_identifier"], row[0])
            self.assertTrue(
                engine.execute(
                    "SELECT code FROM station WHERE id = ?", row[1]
                ).fetchall()[0][0]
                in expected_row["participating_stations"]
            )

    @mock.patch("gmn_data_store._DB_CONNECTION_URI", "sqlite://")
    def test_insert_trajectory_summary_existing_station(self) -> None:
        """
        Test: That insert_trajectory_summary() creates the correct row in the Meteor
         table.
        When: insert_trajectory_summary() is called with an existing station.
        """
        data_frame = gmn_python_api.read_trajectory_summary_as_dataframe(
            gmn_python_api.trajectory_summary_schema._MODEL_TRAJECTORY_SUMMARY_FILE_PATH,
            avro_compatible=True,
        )

        engine = gmn_data_store.setup_database.setup_database()
        expected_row = data_frame.iloc[0].to_dict()

        # Test adding an existing station
        engine.execute("INSERT INTO station (code) VALUES ('TEST')")
        expected_row["participating_stations"].append("TEST")
        gmn_data_store.controller.insert_trajectory_summary(expected_row, engine)

        # Test if TEST only appears once in the station table
        self.assertEqual(
            1,
            engine.execute(
                "SELECT COUNT(*) FROM station WHERE code = ?", ("TEST",)
            ).fetchall()[0][0],
        )
