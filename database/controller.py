from datetime import datetime

from __init__ import get_engine
from sqlalchemy.orm import sessionmaker

from models import Trajectory, Station, ParticipatingStation

db = get_engine()


class DatabaseController:
    def __init__(self):
        self.db_session_maker = sessionmaker(bind=db)

    def get_all_rows_of_table(self, table):
        db_session = self.db_session_maker()
        rows = db_session.query(table).all()
        db_session.close()
        return rows

    def get_row_by_id_of_table(self, table, id: int):
        db_session = self.db_session_maker()
        row = db_session.query(table).filter_by(id=id).first()
        db_session.close()
        return row

    def create_row(self, table, **fields):
        db_session = self.db_session_maker()
        row = table(**fields)
        exists = db_session.query(table).filter_by(id=fields['id']).first()
        if not exists:
            db_session.add(row)
        db_session.commit()
        db_session.close()

    def insert_trajectory_summary(self, row_dict):
        db_session = self.db_session_maker()

        main_meteor_props = [
            'beginning_utc_time',
            'latbeg_n_deg',
            'lonbeg_e_deg',
            'htbeg_km',
            'rageo_deg',
            'decgeo_deg',
            'vgeo_km_s'
        ]
        other_excluded_data_jsonb_props = [
            'beginning_julian_date',
            'iau_no',
            'iau_code'
            'schema_version',
            'participating_stations',
            'num_stat'
        ]

        data_jsonb = {k: row_dict[k] for k in set(list(row_dict.keys())) - set(main_meteor_props)}
        data_jsonb = {k: data_jsonb[k] for k in set(list(data_jsonb.keys())) - set(other_excluded_data_jsonb_props)}

        main_data_fields = {}
        for main_prop in main_meteor_props:
            main_data_fields[main_prop] = row_dict[main_prop]

        main_data_fields["beginning_utc_time"] = datetime.utcfromtimestamp(main_data_fields["beginning_utc_time"] / 1e6)

        trajectory_row = db_session.merge(Trajectory(
            # meteor_id=row_dict["meteor_id"],
            data=data_jsonb,
            data_schema_version = row_dict["schema_version"],
            iau_shower_id = None if row_dict["iau_no"] == -1 else row_dict["iau_no"],
            **main_data_fields
        ))

        # db_session.flush()
        db_session.commit()

        for station_code in row_dict["participating_stations"]:
            # if a station doesn't exist in the db with the same station_code
            existing_station = db_session.query(Station).filter_by(code=station_code).first()
            if not existing_station:
                station_row = db_session.merge(Station(
                    code = station_code
                ))
                # db_session.flush()
                db_session.commit()
                station_id = station_row.id
            else:
                station_id = existing_station.id

            if not db_session.query(ParticipatingStation).filter_by(
                    trajectory_id=trajectory_row.id, station_id=station_id).first():
                participating_station_row = db_session.merge(ParticipatingStation(
                    trajectory_id = trajectory_row.id,
                    station_id = station_id
                ))
                # db_session.flush()
                db_session.commit()

        db_session.close()
