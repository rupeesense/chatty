from typing import Literal, Union

from langchain import SQLDatabase


class CustomSQLDatabase(SQLDatabase):

    def run(
            self,
            command: str,
            fetch: Union[Literal["all"], Literal["one"]] = "all",
    ) -> str:
        """Execute a SQL command and return a string representing the results.

        If the statement returns rows, a string of the results is returned.
        If the statement returns no rows, an empty string is returned.
        """
        result = self._execute(command, fetch)
        return result
