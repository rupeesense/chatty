from sqlalchemy import Column, String, DateTime, Float, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserSavings(Base):
    __tablename__ = 'user_savings'

    user_id = Column(String(50), primary_key=True, nullable=False)
    account_id = Column(String(50), primary_key=True, nullable=False)
    record_date = Column(DateTime, primary_key=True, nullable=False)
    savings_delta = Column(Float, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'account_id', 'record_date'),
    )
