import os
import tempfile
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.sitemap import SitemapLoader
from langchain_community.vectorstores import SKLearnVectorStore
#from langchain_openai import OpenAIEmbeddings
from langsmith import traceable
#from openai import OpenAI
from typing import List
import nest_asyncio

MODEL_NAME = "gemini-2.5-flash"
MODEL_PROVIDER = "google"
APP_VERSION = 1.0
RAG_SYSTEM_PROMPT = """You are an assistant for question-answering tasks. 
Use the following pieces of retrieved context to answer the latest question in the conversation. 
If you don't know the answer, just say that you don't know. 
Use three sentences maximum and keep the answer concise.
"""

import os
from google import genai
# openai_client = OpenAI()
client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

from langchain_community.embeddings import HuggingFaceEmbeddings

def get_vector_db_retriever():
    """
    Creates or loads a scikit-learn based vector store retriever.
    
    This function replaces OpenAIEmbeddings with a local, open-source model
    from Hugging Face (sentence-transformers/all-MiniLM-L6-v2) for generating
    document embeddings.

    Returns:
        A retriever object for querying the vector store.
    """
    persist_path = os.path.join(tempfile.gettempdir(), "union_local.parquet")
    
    # Initialize a local, open-source embedding model from Hugging Face.
    # This model runs on your machine and does not require an API key.
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    model_kwargs = {'device': 'cpu'} # Use CPU for embedding
    encode_kwargs = {'normalize_embeddings': False}
    embd = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )

    # If vector store exists, then load it
    if os.path.exists(persist_path):
        print(f"Loading existing vector store from: {persist_path}")
        vectorstore = SKLearnVectorStore(
            embedding=embd,
            persist_path=persist_path,
            serializer="parquet"
        )
        # lambda_mult=0 is used for Maximal Marginal Relevance (MMR) search.
        # It effectively disables MMR and performs a standard similarity search.
        return vectorstore.as_retriever(lambda_mult=0)

    # Otherwise, index LangSmith documents and create a new vector store
    print("No existing vector store found. Indexing documents...")
    ls_docs_sitemap_loader = SitemapLoader(
        web_path="https://docs.smith.langchain.com/sitemap.xml", 
        continue_on_failure=True,
        # Optional: Filter URLs to only include relevant documentation pages
        # filter_urls=["https://docs.smith.langchain.com/"]
    )
    
    # Set a custom user-agent to be respectful when scraping
    ls_docs_sitemap_loader.headers = {
        "User-Agent": "LocalVectorDBBuilder/1.0 (https://example.com/bot-info)"
    }
    ls_docs = ls_docs_sitemap_loader.load()

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=500, chunk_overlap=100 # Increased overlap for better context
    )
    doc_splits = text_splitter.split_documents(ls_docs)
    
    print(f"Created {len(doc_splits)} document splits. Creating vector store...")

    vectorstore = SKLearnVectorStore.from_documents(
        documents=doc_splits,
        embedding=embd,
        persist_path=persist_path,
        serializer="parquet"
    )
    
    print(f"Persisting vector store to: {persist_path}")
    vectorstore.persist()
    return vectorstore.as_retriever(lambda_mult=0)


nest_asyncio.apply()
retriever = get_vector_db_retriever()

"""
retrieve_documents
- Returns documents fetched from a vectorstore based on the user's question
"""
@traceable(run_type="chain")
def retrieve_documents(question: str):
    return retriever.invoke(question)

"""
generate_response
- Calls `call_openai` to generate a model response after formatting inputs
"""
@traceable(run_type="chain")
def generate_response(question: str, documents):
    formatted_docs = "\n\n".join(doc.page_content for doc in documents)
    # messages = [
    #     {
    #         "role": "system",
    #         "content": RAG_SYSTEM_PROMPT
    #     },
    #     {
    #         "role": "user",
    #         "content": f"Context: {formatted_docs} \n\n Question: {question}"
    #     }
    # ]
    messages = [
                  {
                      "role": "user",
                      "parts": [
                          {"text": RAG_SYSTEM_PROMPT},
                          {"text": f"Context: {formatted_docs} \n\n Question: {question}"}
                      ]
                  }
              ]
    return call_gemini(messages)

"""
call_gemini
- Returns the chat completion output from OpenAI
"""
@traceable(
    run_type="llm",
    metadata={
        "ls_provider": MODEL_PROVIDER,
        "ls_model_name": MODEL_NAME
    }
)
def call_gemini(messages: List[dict]) -> str:
    # return openai_client.chat.completions.create(
    #     model=MODEL_NAME,
    #     messages=messages,
    # )
    return client.models.generate_content(
    model=MODEL_NAME, contents=messages
    )

"""
langsmith_rag
- Calls `retrieve_documents` to fetch documents
- Calls `generate_response` to generate a response based on the fetched documents
- Returns the model response
"""
@traceable(run_type="chain")
def langsmith_rag(question: str):
    documents = retrieve_documents(question)
    response = generate_response(question, documents)
    # return response.choices[0].message.content
    return response.candidates[0].content.parts[0].text
