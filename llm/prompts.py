PROMPT_TXN_CATEGORISATION = '''

You are now a transaction categorisation engine. Given a transaction remark, you have to tell what could be the 
merchantId in the remark and what could be the possible category of this merchant. 

If you are not sure about the category of a particular transaction, just say "unknown" category.
Possible categories are listed below. But there could be more.

Housing
Transportation
Food
Healthcare
Debt
Entertainment
Utilities
Savings
Insurance
Personal Care
Education
Charitable Contributions
Childcare
Taxes
Transportation
Insurance
Miscellaneous


Examples:

UPI/228637448244/charge/uberrides@hdfcb/HDFC BANK LTD/HDF5D842C5B5698449D88E34E	
{"merchantId": "uberrides@hdfcb",  category: "Transport"}

UPI/303669057243/Swiggy Order Id/swiggyupi@axisb/Axis Bank Ltd./AXISSDKV3df1698
{"merchantId": "swiggyupi@axisb", "category": "Food"}

ACH/Groww/3HNEHPMPJIQQ
{"merchantId": "Groww", "category": "Investments"}

BIL/NEFT/000456187661/Nps/NPS trust /UTIB0CCH274
{"merchantId": "NPS trust", "category": "Investments"}

UPI/221282547096/Payment from Ph/paytmqr28100505/Paytm Payments /IBL379dd0f5f2c
{"merchantId": "paytmqr28100505", "category": "Unknown"}

UPI/223707214923/payment on CRED/cred.club@axisb/Axis Bank Ltd./ACDjyRLwVvmZEde
{"merchantId": "cred.club@axisb", "category": "Credit Card Payment"}

UPI/223801366873/OidZTDUPIC22A5D/zomato-order@pa/Paytm Payments /PTM20220826357
{"merchantId": "zomato-order@pa", "category": "Food"}

You have to now predict the merhcantId and category for the following transactions:
UPI/300288545508/Payment from Ph/dunzo.payu@hdfc/HDFC BANK LTD/IBL8aa22f7206d54
NEFT-N061232353749944-FUTURE GENERALI INDIA INSURANCE CO-237201001726-006003501


'''
