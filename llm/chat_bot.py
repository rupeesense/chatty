from typing import List

from langchain.chains import LLMChain
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate, \
    AIMessagePromptTemplate

from llm.llm_factory import LLMFactory


class Chatty:

    def __init__(self):
        self.llm = LLMFactory().get_chat_llm()
        template = "You are a helpful assistant that translates that answers user queries respectfully."
        system_message_prompt = SystemMessagePromptTemplate.from_template(template)
        human_template = "{text}"
        ai_message_prompt = AIMessagePromptTemplate.from_template("")
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt, ai_message_prompt])
        self.llm_chain = LLMChain(prompt=chat_prompt, llm=self.llm, verbose=True)

    def respond(self, message: str, chat_history: List[str] = None) -> str:
        return self.llm_chain.run(text=message)
