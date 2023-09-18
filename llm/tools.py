from datetime import time
from typing import Type

from langchain.tools import BaseTool
from pydantic import BaseModel, Field

from llm.features import get_savings_for_a_time_range


class SavingsInput(BaseModel):
    """Inputs for get_savings"""

    from_date: time = Field(description="lower limit of date range to get savings for")
    to_date: time = Field(description="upper limit of date range to get savings for")


class SavingsTool(BaseTool):
    name = "get_savings"
    description = """
        Useful when you want to get the non-aggregated information related to savings for a user in a given time period.  
        """
    args_schema: Type[BaseModel] = SavingsInput

    def _run(self, from_date: time, to_date: time):
        return get_savings_for_a_time_range(from_date, to_date)

    def _arun(self, ticker: str):
        raise NotImplementedError("get_savings does not support async")
