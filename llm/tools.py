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
