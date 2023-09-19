from typing import List

from context_store.document.account_savings_document import AccountSavingsDocument


class UserDocument:
    """
    An instance of this class represents the all the financial information that we have for the user.

    """

    def __int__(self, savings_documents: List[AccountSavingsDocument] = None):
        self.saved_documents = savings_documents if savings_documents else []
