from sqlalchemy import Table, Column, Integer, String, DateTime, func, MetaData
from sqlalchemy.sql import insert

from app.database import engine as chatty_db_engine


class LLMLogger:
    def __init__(self):
        self.engine = chatty_db_engine
        metadata = MetaData()
        self.logs = Table(
            'llm_logs',
            metadata,
            Column('id', Integer, primary_key=True),
            Column('timestamp', DateTime, default=func.now()),
            Column('use_case', String(100)),
            Column('prompt', String(200)),
            Column('response', String(200)),
        )

    def log(self, use_case: str, prompt: str, response: str):
        try:
            stmt = insert(self.logs).values(use_case=use_case, prompt=prompt, response=response)
            with self.engine.connect() as conn:
                conn.execute(stmt)
        except Exception as e:
            print(e)
            pass
