from typing import Type

from langchain.tools import BaseTool
from pydantic import BaseModel, Field

from context_store.context_store import get_savings_documents_by_user_id
from context_store.document.account_savings_document import AccountSavingsDocument


class SavingsInput(BaseModel):
    """Inputs for get_savings"""

    user_id: str = Field(description="user_id for the user whose savings are to be retrieved")


class SavingsTool(BaseTool):
    name = "get_savings"
    description = """
        Useful when you want to get the information related to savings for a user in a given time period.  
        """
    args_schema: Type[BaseModel] = SavingsInput

    def _run(self, user_id: str):
        documents = get_savings_documents_by_user_id("user1")
        json_output = AccountSavingsDocument.objects(id__in=[doc.id for doc in documents]).to_json()
        return json_output

    def _arun(self):
        raise NotImplementedError("get_savings does not support async")


class FactualInput(BaseModel):
    """Inputs for get_factual"""

    fact_key: str = Field(description="fact_key for the fact whose value is to be retrieved, possible values are: "
                                      "interest_rate, recommended_savings_rate")


class FactualTool(BaseTool):
    name = "get_factual"
    description = """
        Useful when you want to get the value of a fact.  
        """
    args_schema: Type[BaseModel] = FactualInput

    def _run(self, fact_key: str):
        if fact_key == "interest_rate":
            return "7 percent per annum"
        elif fact_key == "recommended_savings_rate":
            return "0.2 percent per month"
        else:
            raise ValueError(f"fact_key: {fact_key} is not supported")

    def _arun(self):
        raise NotImplementedError("get_factual does not support async")
