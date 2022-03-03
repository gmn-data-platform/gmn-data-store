from database import get_engine
from sqlalchemy.orm import sessionmaker

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
        db_session.add(row)
        db_session.commit()
        db_session.close()
