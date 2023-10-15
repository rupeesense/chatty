from langchain.chains import create_sql_query_chain
from langchain.prompts import PromptTemplate

from context_store.custom_sql_database import CustomSQLDatabase
from context_store.llm_logger import llm_logger
from llm.llm_factory import LLMFactory

examples = [
    # 'savings for September',
    'month with lowest savings so far this year',
    'savings rate for september',
]


# fql stands for flexible query language
class FQLEngine:
    fql_engine_template = '''You are a MySQL expert. Given an input question, first create a syntactically correct MySQL query to run, then look at the results of the query and return the answer to the input question.You can order the results to return the most informative data in the database.
Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in backticks (`) to denote them as delimited identifiers.
Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
If the query requires only one row, use LIMIT clause to limit the number of rows returned to 1.

Use the following format:
Question: Question here
SQLQuery: SQL Query to run
SQLResult: Result of the SQLQuery

Some examples of SQL queries that correspond to questions are:
Question: savings for august for user: xyz
SQLQuery: SELECT savings_delta as savings_august FROM user_account_monthly_records WHERE user_id = 'xyz' AND month(date) = '8' and year(date)='2023' limit 1;

Question: month with highest savings so far this year for user: xyz
SQLQuery: SELECT month(date) as highest_savings_month, savings_delta as highest_savings_amount FROM user_account_records WHERE user_id = 'xyz' and year(date)='2023' ORDER BY savings_delta DESC LIMIT 1;

Question: percentage of income saved for accountA in september for user: xyz
SQLQuery: SELECT (savings_delta/income)*100 as percentage_income_saved FROM user_account_monthly_records WHERE user_id = 'xyz' AND month(date) = '9' and year(date)='2023' limit 1;

current date is 2023-10-14.
Only use the following tables:
user_account_monthly_records: contains only one record per month per user and per account.
{table_info}

Now answer the following question:
Question: {input}'''

    CUSTOM_TEMPLATE = PromptTemplate(
        input_variables=["input", "table_info"],
        template=fql_engine_template,
    )

    def __init__(self):
        self._tables_names = ["user_account_monthly_records"]
        self._llm = LLMFactory().get_fql_llm()
        self.db = CustomSQLDatabase.from_uri('mysql+pymysql://root:@localhost:3306/feature_store',
                                             include_tables=self._tables_names,
                                             sample_rows_in_table_info=3)
        self._chain = create_sql_query_chain(self._llm,
                                             self.db,
                                             prompt=self.CUSTOM_TEMPLATE)

    # this function takes in a fql and returns a response
    # fql is represented in english language and contains the argument along with time range
    def run(self, fql: str, user_id: str):
        query = fql + " for user: " + user_id
        print(query)
        sql_query = self._chain.invoke({"question": query,
                                        "table_names_to_use": self._tables_names})
        result = self.db.run(sql_query)
        llm_logger.log(use_case='fql_to_sql', prompt=fql, response=sql_query, llm_params=self._llm._default_params)
        print(result)
        return result


if __name__ == '__main__':
    fql_engine = FQLEngine()
    for example in examples:
        fql_engine.run(example, 'xyz')
