from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.engine import Connection
from app.core.database.tables.sample_tables import SampleTable, SampleAddress
from app.shared.db_utils.save_data import commit_and_refresh, commit_function, sql_commit_and_refresh, sql_commit_function
from app.shared.logger.setup import app_logger
from sqlalchemy import insert, update, select, delete, join


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
        # import pdb;pdb.set_trace()
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
        
class SqlSampleService:
    def __init__(self, connection : Connection):
        self.connection = connection
        self.transaction = connection.begin()

    def add_new(self, name:str):
        # import pdb;pdb.set_trace()
        new_data = insert(SampleTable).values(name=name).returning(SampleTable)
        obj = self.connection.execute(new_data)
        try:
            return sql_commit_and_refresh(transaction = self.transaction, obj=obj)
        except Exception as e:
            app_logger.error(e)
            raise HTTPException(status_code=500, detail='Internal Server Error')
        
    def update_sample(self, id:int, name: str):
        update_data = update(SampleTable).where(SampleTable.id == id).values(name= name).returning(SampleTable)
        obj = self.connection.execute(update_data)
        # self.connection.execute(text("""update sample_table set name = """+str(name)+""" where id = """+ str(id)+""""""))
        try:
            return sql_commit_and_refresh(transaction = self.transaction, obj=obj)
        except Exception as e:
            app_logger.error(e)
            raise HTTPException(status_code=404, detail='Not found')
        
    def get_sample(self, id:int):
        # self.connection.execute(text("""select id, name from sample_table where id = """+str(id)+""""""))
        # get_data = select(SampleTable).where(SampleTable.id == id)
        # obj = self.connection.execute(get_data)
        
        join_query = join(SampleTable, SampleAddress, SampleTable.id == SampleAddress.sample_id) 
        select_query = select(SampleTable.id, SampleTable.name, SampleAddress.address).select_from(join_query).where(SampleTable.id == id)
        obj = self.connection.execute(select_query)
        
        try:
            return sql_commit_and_refresh(transaction = self.transaction, obj=obj)
        except Exception as e:
            app_logger.error(e)
            raise HTTPException(status_code=404, detail='Not found')
        
    def delete_sample(self, id:int):
        # self.connection.execute(text("""delete from sample_table where id="""+str(id)+""""""))
        delete_data = delete(SampleTable).where(SampleTable.id == id)
        self.connection.execute(delete_data)
        try:
            self.connection.execute(delete_data)
            return sql_commit_function(transaction = self.transaction)
        except Exception as e:
            app_logger.error(e)
            raise HTTPException(status_code=404, detail='Not found')