from mongoengine import connect, disconnect

from context_store.document.account_savings_document import AccountSavingsDocument


def get_savings_documents_by_user_id(user_id: str):
    return list(AccountSavingsDocument.objects(user_id=user_id))


class ContextStore:
    def __init__(self, db_name='context_store', host='localhost', port=27017, **kwargs):
        """
        Initialize MongoDBManager with connection details.

        :param db_name: Name of the database to connect to.
        :param host: Hostname of the MongoDB server. Default is 'localhost'.
        :param port: Port of the MongoDB server. Default is 27017.
        :param kwargs: Additional arguments to pass to mongoengine.connect.
        """
        self.db_name = db_name
        self.host = host
        self.port = port
        self.kwargs = kwargs

    def connect(self):
        """
        Establish the connection to the MongoDB server.
        """
        connect(db=self.db_name, host=self.host, port=self.port, **self.kwargs)

    def disconnect(self):
        """
        Disconnect from the MongoDB server.
        """
        disconnect()
