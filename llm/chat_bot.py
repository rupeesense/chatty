from langchain.chains import LLMChain
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate, \
    AIMessagePromptTemplate, PromptTemplate

from context_store.llm_logger import llm_logger
from llm.llm_factory import LLMFactory

PROMPT = '''<s>[INST]You are a helpful personal finance assistant that translates that answers user queries respectfully.
Try to explain the numbers in a helpful manner. You have to report all numbers in rupees.

{history}
Human: {text}
Context: {context}
AI: [/INST]'''


class Chatty:

    def __init__(self):
        self._llm = LLMFactory().get_chat_llm()
        sys_prompt = "You are a helpful personal finance assistant that translates that answers user queries respectfully." \
                     " Try to explain the numbers in a helpful manner. You have to report all numbers in rupees."
        system_message_prompt = SystemMessagePromptTemplate.from_template(sys_prompt)
        human_message_prompt = HumanMessagePromptTemplate.from_template("{text}")
        ai_message_prompt = AIMessagePromptTemplate.from_template("")
        prev_conv_prompt = ChatPromptTemplate.from_template("history of conversation: {history}")
        context_prompt = ChatPromptTemplate.from_template(
            "You can use the following information to answer human query: {context}")
        chat_prompt = ChatPromptTemplate.from_messages(
            [system_message_prompt,
             prev_conv_prompt,
             human_message_prompt,
             context_prompt,
             ai_message_prompt])
        custom_template = PromptTemplate(input_variables=["history", "text", "context"], template=PROMPT)
        self._llm.bind(stop=["\n\n"])
        self.llm_chain = LLMChain(prompt=custom_template, llm=self._llm, verbose=True)

    def respond(self, message: str, context: str, chat_history: str) -> str:
        if chat_history is not "":
            chat_history = "history of conversation: \n" + chat_history
        model_response = self.llm_chain.run(text=message, context=context, history=chat_history)
        llm_logger.log(use_case='chatty', prompt=message, response=model_response, llm_params=self._llm._default_params)
        return model_response
