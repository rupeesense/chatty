from typing import List

from langchain.chains import LLMChain
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate, \
    AIMessagePromptTemplate

from llm.llm_factory import LLMFactory


class Chatty:

    def __init__(self):
        self.llm = LLMFactory().get_chat_llm()
        sys_prompt = "You are a helpful assistant that translates that answers user queries respectfully." \
                     " Try to explain the numbers in a helpful manner."
        system_message_prompt = SystemMessagePromptTemplate.from_template(sys_prompt)
        human_message_prompt = HumanMessagePromptTemplate.from_template("{text}")
        ai_message_prompt = AIMessagePromptTemplate.from_template("")
        context_prompt = ChatPromptTemplate.from_template(
            "You can use the following information to answer human query: {context}")
        chat_prompt = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_message_prompt, context_prompt, ai_message_prompt])
        self.llm_chain = LLMChain(prompt=chat_prompt, llm=self.llm, verbose=True)

    def respond(self, message: str, context: str, chat_history: List[str] = None) -> str:
        return self.llm_chain.run(text=message, context=context)
