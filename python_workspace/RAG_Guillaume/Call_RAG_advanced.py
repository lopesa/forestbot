import os
from dotenv import load_dotenv, find_dotenv
import openai

#sys.path.append('../..')

env_path = find_dotenv()

_ = load_dotenv(find_dotenv()) # read local .env file

os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY', 'Default_API_Key')

openai.api_key  = os.environ['OPENAI_API_KEY']

#openai.api_key = os.environ['OPENAI_API_KEY']


# Index
from langchain_openai import OpenAIEmbeddings
persist_directory="vectorstore/chroma"

from langchain_community.vectorstores import Chroma

vectorstore = Chroma(persist_directory=persist_directory, embedding_function=OpenAIEmbeddings())

retriever = vectorstore.as_retriever()

