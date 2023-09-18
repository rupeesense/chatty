from datetime import date
from typing import Dict

from context_store.models.user_savings import UserSavings


class SavingsRecord:
    def __init__(self, record_date: date, savings_delta: float):
        self.record_date = record_date
        self.savings_delta = savings_delta


class AccountSavingsDocument:
    """
    An instance of this class represents the savings of a user over time for a particular account.

    """

    def __int__(self, account_id: str, total_savings: float = 0.0, savings_records: Dict[date, SavingsRecord] = None):
        self.account_id = account_id
        self.total_savings = total_savings
        self.savings_records = savings_records if savings_records else {}

    @classmethod
    def from_records(cls, user_saving_records: [UserSavings]) -> Dict[str, "AccountSavingsDocument"]:
        accounts_data = {}

        for record in user_saving_records:
            if record.account_id not in accounts_data:
                accounts_data[record.account_id] = {
                    "total_savings": 0.0,
                    "savings_records": {}
                }

            accounts_data[record.account_id]["total_savings"] += record.savings_delta

            # TODO: will we need to convert b/w date types here?
            savings_record = SavingsRecord(record_date=record.record_date, savings_delta=record.savings_delta)
            accounts_data[record.account_id]["savings_records"][record.record_date] = savings_record

        return {
            account_id: AccountSavingsDocument(
                account_id=account_id,
                total_savings=data["total_savings"],
                savings_records=data["savings_records"]
            )
            for account_id, data in accounts_data.items()
        }
