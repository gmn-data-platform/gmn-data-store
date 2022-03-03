import os
import json
import pandavro as pdx
from avro.datafile import DataFileReader
from avro.io import DatumReader
from gmn_python_api.trajectory_summary_reader import \
    read_trajectory_summary_as_dataframe

AVRO_PATH = '{}/trajectory_summary_schema.avro'.format(os.path.dirname(__file__))
AVSC_PATH = '{}/trajectory_summary_schema.avsc'.format(os.path.dirname(__file__))


def main():
    df = read_trajectory_summary_as_dataframe("trajectory_summary_replica.txt")
    df['IAU (code)'] = df['IAU (code)'].astype('unicode')
    df['Participating (stations)'] = df['Participating (stations)'].astype('unicode')

    pdx.to_avro(AVRO_PATH, df)
    saved = pdx.read_avro(AVRO_PATH)
    print(saved)

    reader = DataFileReader(open(AVRO_PATH, "rb"),
                            DatumReader())
    schema = json.loads(reader.meta['avro.schema'].decode())
    print(schema)

    with open(AVSC_PATH, 'w') as f:
        json.dump(schema, f, indent=2)


if __name__ == '__main__':
    main()
