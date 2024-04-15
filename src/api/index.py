from flask import Flask, request
# from dotenv import load_dotenv
# import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# env = os.environ


chat = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0.2)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. Answer all questions to the best of your ability.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

chain = prompt | chat



app = Flask(__name__)

@app.route("/api/chat", methods=['POST'])
def main():
    test = chain.invoke(
      {
          "messages": request.json['messages'],
      }
    )
    try:
        res = test.content
    except:
        res = 'Error'
    return res