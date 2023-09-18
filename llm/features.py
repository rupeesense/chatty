from datetime import time

SAVINGS_QUERY = '''

SELECT record_date, savings_delta FROM user_savings
 WHERE user_id = 'aviral.verma' AND account_id = '12345211'
  AND record_date >= '{{ from_date }}' AND record_date < '{{ to_date }}'
  ORDER BY record_date ASC LIMIT 10

'''


def get_savings_for_a_time_range(from_date: time, to_date: time):
    pass
