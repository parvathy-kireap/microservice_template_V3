from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.database.tables.sample_tables import SampleTable
from app.shared.db_utils.save_data import commit_and_refresh, commit_function
from app.shared.logger.setup import app_logger


class SampleService:
    def __init__(self, db: Session):
        self.db = db

    def add_new(self, name: str):
        new_data = SampleTable()
        new_data.name = name

        try:
            self.db.add(new_data)
            return commit_and_refresh(db=self.db, obj=new_data)
        except Exception as e:
            app_logger.error(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")
        
    def update_sample(self, id:int, name:str):
        sample_data = self.db.query(SampleTable).filter(SampleTable.id == id).first()

        try:
            sample_data.name = name
            return commit_and_refresh(db=self.db, obj=sample_data)
        except Exception as e:
            app_logger.error(e)
            raise HTTPException(status_code=404, detail="Not found")

    def get_sample(self, id:int):
        sample_data = self.db.query(SampleTable).filter(SampleTable.id == id).first()

        try:
            return commit_and_refresh(db=self.db, obj=sample_data)
        except Exception as e:
            app_logger.error(e)
            raise HTTPException(status_code=404, detail="Not found")

    def delete_sample(self, id:int):
        self.db.query(SampleTable).filter(SampleTable.id == id).delete()

        try:
            return commit_function(db=self.db)
        except Exception as e:
            app_logger.error(e)
            raise HTTPException(status_code=404, detail="Not found")