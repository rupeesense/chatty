from langchain import SQLDatabase, OpenAI
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType

db = SQLDatabase.from_uri("mysql://root:@localhost:3306/feature_store")
llm = OpenAI(temperature=0, verbose=True)

agent_executor = create_sql_agent(
    llm=OpenAI(temperature=0),
    toolkit=SQLDatabaseToolkit(db=db, llm=llm),
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)

agent_executor.run(
    "How have my monthly savings varied over the past year? Report all numbers in rupees. Try to explain the numbers "
    "in a helpful manner. Today's date is 18th Sept 2023. "
)
