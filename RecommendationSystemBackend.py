import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import BedrockEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.indexes import VectorstoreIndexCreator
from langchain_aws import BedrockLLM
import boto3

def data_ingension_flow():
    policy_data = PyPDFLoader('https://www.coverme.com/content/dam/affinity/coverme/english/documents/sample-contracts-and-certificates/coverme-term-10-life-insurance-policy.pdf')
    data_test = policy_data.load_and_split()
    # print(len(data_test))
    # print(data_test[2])

    policy_data_chunking = RecursiveCharacterTextSplitter(separators=["\n\n", "\n", " ", ""], chunk_size=100, chunk_overlap=10)

    # data_sample = 'Our website uses some cookies and records your IP address for the purposes of accessibility, security, and managing your access to the telecommunication network. You can disable data collection and cookies by changing your browser settings, but it may affect how this website functions. Learn more.'
    # data_split_test = policy_data_chunking.split_text(data_sample)
    # print(data_split_test)

    data_embeddings = BedrockEmbeddings(
        credentials_profile_name="default",
        model_id="amazon.titan-embed-text-v2:0"
    )

    data_index = VectorstoreIndexCreator(vectorstore_cls = FAISS, text_splitter = policy_data_chunking, embedding = data_embeddings)

    db_index = data_index.from_loaders([policy_data])
    return db_index

def connectToBedRock():
    client = boto3.client("bedrock-runtime", region_name="us-east-1")
    llm = BedrockLLM(
        credentials_profile_name="default",
        model_id="cohere.command-r-v1:0",
        model_kwargs={
            "max_tokens_to_sample": 1000,
            "temperature": 0.1,
            "top_p":0.9
        }
    )
    print("This is called ---------")

    return llm

def userRecommendations(index, question):
    llm = connectToBedRock()
    response = index.query(question=question, llm=llm)
    return response
