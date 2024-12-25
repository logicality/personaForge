import os
import shutil
from langchain.schema import Document
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

from storage.storage import JSONDataManager
from storage.config import SIXTEEN_PERSONALITIES_LOC, CLEANSED, CHATGPT_PERSONALITIES_LOC, CHATGPT_TOPIC_DETAILS_LOC
from embed.config import VECTOR_DB_DIR

class VectorStore:
    """
    A class to manage vector store operations.
    """

    def __init__(self, persist_directory: str, collection_name: str = "documents", embedding_function = None):
        """
        Initialize the VectorStore with the given parameters.
        
        Args:
            persist_directory (str): The directory to persist the vector store.
            collection_name (str): The name of the collection in the vector store.
            embedding_function: The function to generate embeddings.
        """
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self.embedding_function = embedding_function

        # Ensure the vector database directory exists
        os.makedirs(self.persist_directory, exist_ok=True)

        # Initialize the vector store
        self.vectorstore = Chroma(
            collection_name=self.collection_name,
            persist_directory=self.persist_directory,
            embedding_function=self.embedding_function
        )

    def add_documents(self, docs: list):
        """
        Add documents to the vector store.
        
        Args:
            docs (list): A list of documents to add.
        """
        self.vectorstore.add_documents(docs)

    def reset(self):
        """
        Reset the vector database.
        """
        shutil.rmtree(self.persist_directory, ignore_errors=True)
        os.makedirs(self.persist_directory, exist_ok=True)

        # Reinitialize the vector store
        self.vectorstore = Chroma(
            collection_name=self.collection_name,
            persist_directory=self.persist_directory,
            embedding_function=self.embedding_function
        )
        print(f"Vector store at '{self.persist_directory}' has been reset.")

    def query(self, query: str, top_k: int = 5):
        """
        Query the vector store.
        
        Args:
            query (str): The query string.
            top_k (int): The number of top results to return.
        
        Returns:
            list: The top_k results from the vector store.
        """
        return self.vectorstore.similarity_search(query, k=top_k)

class Embedder(VectorStore):
    """
    A class to handle embedding and storing text.
    """

    def __init__(self, model_name: str, chunk_size: int, chunk_overlap: int, persist_directory: str):
        """
        Initialize the Embedder with the given parameters.
        
        Args:
            model_name (str): The name of the embedding model.
            chunk_size (int): The size of each text chunk.
            chunk_overlap (int): The overlap between text chunks.
            persist_directory (str): The directory to persist the vector store.
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.model_name = model_name

        # Initialize the embedding function
        self.embedding_function = HuggingFaceEmbeddings(model_name=self.model_name)

        # Pass the embedding function and other params to the base class
        super().__init__(persist_directory, embedding_function=self.embedding_function)

    def chunk_text(self, text: str) -> list:
        """
        Chunk the text into smaller pieces using LangChain's character splitter.
        
        Args:
            text (str): The text to chunk.
        
        Returns:
            list: A list of text chunks.
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len
        )
        return text_splitter.split_text(text)

    def embed_and_store(self, text: str):
        """
        Chunk, embed, and store text.
        
        Args:
            text (str): The text to embed and store.
        """
        chunks = self.chunk_text(text)
        docs = [Document(page_content=chunk, metadata={}) for chunk in chunks]
        self.add_documents(docs)

class VectorStoreManager:
    """
    A class to manage vector store operations for different datasets.
    """

    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50,
                 vector_db_dir: str = VECTOR_DB_DIR, embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize the VectorStoreManager with the given parameters.
        
        Args:
            chunk_size (int): The size of each text chunk.
            chunk_overlap (int): The overlap between text chunks.
            vector_db_dir (str): The directory to persist the vector store.
            embedding_model (str): The name of the embedding model.
        """
        self.embedder = Embedder(
            model_name=embedding_model,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            persist_directory=vector_db_dir
        )

    def reset_vectorstore(self):
        """
        Reset the vector database.
        """
        self.embedder.reset()

    def query_vectorstore(self, query: str, top_k: int = 5):
        """
        Query the vector database.
        
        Args:
            query (str): The query string.
            top_k (int): The number of top results to return.
        
        Returns:
            list: The top_k results from the vector store.
        """
        return self.embedder.query(query, top_k=top_k)

    def sixteen_personality_embed(self):
        """
        Embed and store sixteen personality data.
        """
        storage_manager = JSONDataManager(CLEANSED, SIXTEEN_PERSONALITIES_LOC)
        files = storage_manager.get_files()

        for file in files:
            data = storage_manager.load_json(file)
            for key, value in data.items():
                if key == 'ptype':
                    continue
                self.embedder.embed_and_store(value)

    def chatGPT_personality_embed(self):
        """
        Embed and store ChatGPT personality data.
        """
        storage_manager = JSONDataManager(CLEANSED, CHATGPT_PERSONALITIES_LOC)
        files = storage_manager.get_files()

        for file in files:
            data = storage_manager.load_json(file)
            for key, value in data.items():
                self.embedder.embed_and_store(value)

    def chatGPT_topic_embed(self):
        """
        Embed and store ChatGPT topic data.
        """
        storage_manager = JSONDataManager(CLEANSED, CHATGPT_TOPIC_DETAILS_LOC)
        files = storage_manager.get_files()

        for file in files:
            data = storage_manager.load_json(file)
            for key, value in data.items():
                self.embedder.embed_and_store(f"{key}: {value}")
