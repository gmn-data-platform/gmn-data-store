import os
import json
import pandavro as pdx
from avro.datafile import DataFileReader
from avro.io import DatumReader
from gmn_python_api.trajectory_summary_reader import \
    read_trajectory_summary_as_dataframe, DATETIME_FORMAT

SCHEMA_VERSION = 1
AVRO_PATH = f'{os.path.dirname(__file__)}/trajectory_summary_schema_{SCHEMA_VERSION}.avro'
AVSC_PATH = f'{os.path.dirname(__file__)}/trajectory_summary_schema_{SCHEMA_VERSION}.avsc'


def main():
    df = read_trajectory_summary_as_dataframe("trajectory_summary_replica.txt")
    df['IAU (code)'] = df['IAU (code)'].astype('unicode')
    df['Participating (stations)'] = df['Participating (stations)'].astype('unicode')
    df['Participating (stations)'] = df['Participating (stations)'].apply(lambda x: x[1:-1].split(','))
    # df['Beginning (UTC Time)'] = df['Beginning (UTC Time)'].dt.strftime(DATETIME_FORMAT+".%f")
    print(df['Beginning (UTC Time)'].dtype)
    print(df['Beginning (UTC Time)'].head())

    df.columns = df.columns.str.replace('[^0-9a-zA-Z]+', '_')
    df.columns = df.columns.str.rstrip('_')
    df.columns = df.columns.str.lstrip('_')
    df.columns = df.columns.str.replace('Q_AU', 'q_au_')
    df.columns = df.columns.str.lower()

    df['schema_version'] = SCHEMA_VERSION
    df.schema_version = df.schema_version.astype('int')

    print(df.info())

    pdx.to_avro(AVRO_PATH, df)
    saved = pdx.read_avro(AVRO_PATH)
    print(saved)

    reader = DataFileReader(open(AVRO_PATH, "rb"),
                            DatumReader())
    schema = json.loads(reader.meta['avro.schema'].decode())

    with open(AVSC_PATH, 'w') as f:
        json.dump(schema, f, indent=2)


if __name__ == '__main__':
    main()
