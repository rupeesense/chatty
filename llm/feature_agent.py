from langchain import OpenAI
from langchain.agents import initialize_agent
from langchain.agents.agent_types import AgentType

from context_store.context_store import ContextStore
from llm.tools import SavingsTool

if __name__ == '__main__':
    ContextStore().connect()

    tools = [SavingsTool()]

    agent_executor = initialize_agent(
        tools=tools,
        llm=OpenAI(temperature=0, openai_api_key='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'),
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    )

    # agent_executor.run(
    #     "How have my monthly savings varied over the past year? Report all numbers in rupees. Try to explain the numbers "
    #     "in a helpful manner. Today's date is 19th Sept 2023. My user_id is: user1."
    # )

    agent_executor.run(
        "What is my total savings across all bank accounts? Report all numbers in rupees. Try to explain the numbers "
        "in a helpful manner. Today's date is 19th Sept 2023. My user_id is: user1."
    )
