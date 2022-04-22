# Database Schema

```mermaid
erDiagram

  iau_shower {
    INTEGER id
    VARCHAR code
    VARCHAR name
    DATETIME created_at
    DATETIME updated_at
  }

  station {
    INTEGER id
    VARCHAR code
    DATETIME created_at
    DATETIME updated_at
  }

  meteor {
    VARCHAR id
    DATETIME created_at
    DATETIME updated_at
    VARCHAR schema_version
    INTEGER iau_shower_id
    FLOAT beginning_julian_date
    DATETIME beginning_utc_time
    FLOAT sol_lon_deg
    FLOAT app_lst_deg
    FLOAT rageo_deg
    CUT_METEOR_PROPERTIES other_meteor_properties
  }

  participating_station {
    INTEGER id
    DATETIME created_at
    DATETIME updated_at
    VARCHAR meteor_id
    INTEGER station_id
  }

  meteor_summary {
    VARCHAR unique_trajectory_identifier
    FLOAT beginning_julian_date
    DATETIME beginning_utc_time
    INTEGER iau_no
    VARCHAR iau_code
    INT num_stat
    ARRAY participating_stations
    VARCHAR schema_version
    FLOAT sol_lon_deg
    FLOAT app_lst_deg
    FLOAT rageo_deg
    CUT_METEOR_PROPERTIES other_meteor_properties
  }

  iau_shower ||--o{ meteor : "iau_shower_id"

  station ||--o{ participating_station : "station_id"

  meteor ||--o{ participating_station : "meteor_id"

```

The tables are generated using the `gmn_python.meteor_summary_schema.get_meteor_summary_avro_schema()` function. `meteor_summary` is an SQLite database view and provides a flat view of all the other meteor related tables. The view includes columns similar to [GMN Data Directory](https://globalmeteornetwork.org/data/) CSVs. The meteor_summary view can be selected using [functions](https://gmn-python-api.readthedocs.io/en/latest/autoapi/gmn_python_api/meteor_summary_reader/index.html#gmn_python_api.meteor_summary_reader.read_meteor_summary_csv_as_dataframe) provided in the `gmn_python_api` package to load meteor data into [Pandas](https://pandas.pydata.org/) DataFrames or [NumPy](https://numpy.org/) arrays through the [GMN REST API](https://github.com/gmn-data-platform/gmn-data-endpoints).

Note that for the diagram `CUT_METEOR_PROPERTIES other_meteor_properties` represents all the other meteor summary properties found in the `gmn-python-api` [Data Schemas](https://gmn-python-api.readthedocs.io/en/latest/data_schemas.html) docs page. Details about the columns can also be found in the Data Schemas page.
