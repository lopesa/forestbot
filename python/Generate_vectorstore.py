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

# Trouver le fichier .env dans le répertoire courant ou remonter jusqu'à ce qu'il soit trouvé
env_path = find_dotenv()
if not env_path:
    raise Exception("Fichier .env non trouvé")

# Charger les variables d'environnement à partir du fichier trouvé
load_dotenv(env_path)

# Vérifier que la clé API nécessaire est chargée
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise EnvironmentError("OPENAI_API_KEY non définie dans le fichier .env")

# Continuer avec l'utilisation de api_key
print("Clé API chargée avec succès.")


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

