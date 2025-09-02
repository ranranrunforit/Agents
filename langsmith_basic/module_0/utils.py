import os
import tempfile
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.sitemap import SitemapLoader
from langchain_community.vectorstores import SKLearnVectorStore
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

# Example of how to use the function
if __name__ == '__main__':
    print("Initializing retriever...")
    retriever = get_vector_db_retriever()
    print("Retriever created successfully.")
    
    # You can now use the retriever to find relevant documents
    query = "What is LangSmith?"
    results = retriever.invoke(query)
    
    print(f"\n--- Top result for query: '{query}' ---")
    if results:
        print(f"Content: {results[0].page_content[:400]}...")
        print(f"Source: {results[0].metadata.get('source', 'N/A')}")
    else:
        print("No results found.")