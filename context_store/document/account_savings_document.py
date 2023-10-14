from mongoengine import Document, StringField, FloatField, DictField, EmbeddedDocument, EmbeddedDocumentField


class SavingsRecord(EmbeddedDocument):
    record_date = StringField(required=True)
    # calculated by subtracting the balance for the previous month from the balance for the current month
    savings_delta = FloatField(required=True, default=0.0)
    # calculated by diving the savings for that month by the income for that user for that month
    savings_income_ratio = FloatField(required=True, default=0.0)
    # calculated by diving the savings for that month by the total savings for that user for that month
    savings_rate = FloatField(required=True, default=0.0)


class AccountSavingsDocument(Document):
    """
    An instance of this class represents the savings of a user over time for a particular account.
    """

    user_id = StringField(required=True)
    account_id = StringField(required=True)
    total_savings = FloatField(required=True, default=0.0)
    savings_records = DictField(EmbeddedDocumentField(SavingsRecord))

    meta = {'collection': 'user_savings'}  # specify the collection name if it's not the same as the class name


if __name__ == '__main__':
    # Instantiate the manager
    # Connect to the database
    from context_store.store import ContextStore
    import random
    from datetime import date, timedelta

    store = ContextStore()
    store.connect()


    def generate_savings_record(months_ago=0, total_savings_for_user=0.0):
        end_date = date(2023, 9, 19) - timedelta(days=30 * months_ago)
        record_date = end_date.strftime("%Y-%m-%d")
        savings_delta = random.uniform(15000, 45000)
        savings_income_ratio = savings_delta / random.uniform(50000, 100000)
        savings_rate = savings_delta / total_savings_for_user

        return record_date, SavingsRecord(record_date=record_date, savings_delta=savings_delta,
                                          savings_income_ratio=savings_income_ratio, savings_rate=savings_rate)


    def generate_savings_record_2(months_ago=0, total_savings_for_user=0.0):
        end_date = date(2023, 9, 19) - timedelta(days=30 * months_ago)
        record_date = end_date.strftime("%Y-%m-%d")
        savings_delta = random.uniform(15000, 45000)
        savings_income_ratio = savings_delta / random.uniform(50000, 100000)
        savings_rate = savings_delta / total_savings_for_user

        record_date_text = "Savings delta for " + record_date + " is " + str(savings_delta) + " rupees. "
        savings_income_ratio_text = "Savings income ratio for " + record_date + " is " + str(
            savings_income_ratio) + " rupees. "
        savings_rate_text = "Savings rate for " + record_date + " is " + str(savings_rate) + " rupees."

        return savings_delta, record_date_text + "\n " + savings_income_ratio_text + "\n " + savings_rate_text + "\n"


    user_ids = ['user1']
    account_ids = ['accountA', 'accountB', 'accountC']

    for uid in user_ids:
        for acc_id in account_ids:
            savings_records_dict = {}
            initial_balance = 30000
            savings_records = ""
            total_savings_for_user = initial_balance
            doc = ""
            for months_ago in range(9):
                savings, record_text = generate_savings_record_2(months_ago, total_savings_for_user)
                savings_records += record_text
                total_savings_for_user += savings

            # doc = AccountSavingsDocument(
            #     user_id=uid,
            #     account_id=acc_id,
            #     total_savings=total_savings_for_user,
            #     savings_records=savings_records_dict
            # )

            doc += "For account: " + acc_id + " total savings are " + str(total_savings_for_user) + " rupees. \n"
            doc += "For account: " + acc_id + " initial balance was " + str(initial_balance) + " rupees. \n"
            doc += "For account: " + acc_id + " savings records for each monther after the initial date was are: \n" + savings_records + "\n"

            print(doc)
            # doc.save()

    # Disconnect from the database (optional, usually at the end of your application or script)
    store.disconnect()
