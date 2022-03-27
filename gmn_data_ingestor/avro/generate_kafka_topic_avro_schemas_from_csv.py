import os
import json
import pandavro as pdx
from avro.datafile import DataFileReader
from avro.io import DatumReader
from gmn_python_api.trajectory_summary_reader import read_trajectory_summary_as_dataframe

SCHEMA_VERSION = "2.0"
AVRO_PATH = f'{os.path.dirname(__file__)}/trajectory_summary_schema_{SCHEMA_VERSION}.avro'
AVSC_PATH = f'{os.path.dirname(__file__)}/trajectory_summary_schema_{SCHEMA_VERSION}.avsc'


def main():
    df = read_trajectory_summary_as_dataframe("trajectory_summary_replica.txt", camel_case_column_names=True)
    df.reset_index(inplace=True)
    df.rename(columns={"Unique trajectory (identifier)": "unique_trajectory_identifier"}, inplace=True)
    df.iau_code = df.iau_code.astype('unicode')
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
