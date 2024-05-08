'''This Python script is designed for managing the vector store used in document processing with langchain libraries. It performs the following key tasks:

1. Environment Setup: Loads necessary environment variables from a .env file, ensuring that the API key for OpenAI is available and valid. This step is crucial for enabling the embedding functionalities that depend on OpenAI's services.

2. Document Loading: Utilizes PyPDFLoader to load PDF documents from specified paths. These documents are then prepared for processing, which involves breaking them down into manageable text segments using a RecursiveCharacterTextSplitter.

3. Vector Store Management:
   - Checks if a pre-existing vector store is available at a specified directory. If it exists, the script loads this vector store to reuse previously computed embeddings.
   - If no vector store is found, the script generates a new one using the loaded and processed documents. This involves creating embeddings for the text segments and storing them in a way that they can be efficiently retrieved for future use.

'''

#########################
###       Import      ###
#########################

import os
from dotenv import load_dotenv, find_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter


#########################
###     Setup API     ###
#########################

# Load the .env file from the current directory or parent directory
load_dotenv(find_dotenv(raise_error_if_not_found=True))

# Retrieve and verify the OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise EnvironmentError("OPENAI_API_KEY not defined in the .env file")

# Use the API key
print("OPENAI_API_KEY successfully loaded.")


#########################
### Load document     ###
#########################
loaders = [
    PyPDFLoader("../pdf/EdAP 2020_EN.pdf"),
    PyPDFLoader("../pdf/SOF book-web-rev3d-hires.pdf"),
]

docs = []
for loader in loaders:
    docs.extend(loader.load())

len(docs)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500, chunk_overlap=50, separators=["\n\n", "\n", "(?<=\. )", " ", ""]
)
splits = text_splitter.split_documents(docs)
print(len(splits))
print(len(docs))

embedding = OpenAIEmbeddings()

persist_directory = "../vectorstore/chroma/"

# Delete the persist_directory if you want to force the generatation of another vector store
#! rm -rf persist_directory


# Check if the vector store already exists
if os.path.exists(persist_directory):
    # If the vector store exists, load it
    vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)

else:
    # If the vector store does not exist, generate it
    # Assuming 'splits' is a list of documents already defined elsewhere in your notebook
    vectordb = Chroma.from_documents(
        documents=splits, embedding=embedding, persist_directory=persist_directory
    )
