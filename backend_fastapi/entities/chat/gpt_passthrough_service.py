from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


class GPTPassthroughService:
    def __init__(self, model_name="gpt-3.5-turbo-1106", temperature=0.2):
        self.chat = ChatOpenAI(model=model_name, temperature=temperature)
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful assistant. Answer all questions to the best of your ability.",
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )

    def process_message(self, messages):
        chain = self.prompt | self.chat
        return chain.invoke(messages)
