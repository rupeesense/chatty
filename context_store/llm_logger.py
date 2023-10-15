from sqlalchemy import Table, Column, Integer, String, DateTime, func, MetaData, JSON
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
            Column('prompt', String(1000)),
            Column('response', String(1000)),
            Column('llm_params', JSON(none_as_null=True)),
        )

    def log(self, use_case: str, prompt: str, response: str, llm_params: dict = None):
        try:
            stmt = insert(self.logs).values(use_case=use_case, prompt=prompt, response=response, llm_params=llm_params)
            with self.engine.connect() as conn:
                conn.execute(stmt)
        except Exception as e:
            print(e)
            pass


llm_logger = LLMLogger()
