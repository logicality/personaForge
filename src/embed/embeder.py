import os
import shutil
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from storage.storage import JSONDataManager
from storage.config import SIXTEEN_PERSONALITIES_LOC, CLEANSED, CHATGPT_PERSONALITIES_LOC
from embed.config import CHUNK_SIZE, CHUNK_OVERLAP, VECTOR_DB_DIR, EMBEDDING_MODEL_NAME

class VectorStoreManager:
    def __init__(self, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP, 
                 vector_db_dir=VECTOR_DB_DIR, embedding_model=EMBEDDING_MODEL_NAME):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.vector_db_dir = vector_db_dir
        self.embedding_model = embedding_model

        # Ensure the vector database directory exists
        os.makedirs(self.vector_db_dir, exist_ok=True)

    def chunk_text(self, text):
        """Chunk the text into smaller pieces using LangChain's character splitter."""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len
        )
        chunks = text_splitter.split_text(text)
        return chunks

    def embed_and_store(self, chunks):
        """Embed chunks and store them in the Chroma vector database."""
        embeddings = HuggingFaceEmbeddings(model_name=self.embedding_model)
        
        vectorstore = Chroma(
            collection_name="documents",
            persist_directory=self.vector_db_dir,
            embedding_function=embeddings
        )

        # Add chunks as documents to the vectorstore
        docs = [Document(page_content=chunk, metadata={}) for chunk in chunks]
        vectorstore.add_documents(docs)

        return vectorstore

    def reset_vectorstore(self):
        """Reset the vector database by deleting and recreating the directory."""
        shutil.rmtree(self.vector_db_dir, ignore_errors=True)
        os.makedirs(self.vector_db_dir, exist_ok=True)

        # Initialize an empty vector store
        embeddings = HuggingFaceEmbeddings(model_name=self.embedding_model)
        vectorstore = Chroma(
            collection_name="documents",
            persist_directory=self.vector_db_dir,
            embedding_function=embeddings
        )

        print(f"Vector store at '{self.vector_db_dir}' has been reset.")

    def query_vectorstore(self, query, top_k=5):
        """Query the vector database to retrieve the most relevant chunks."""
        embeddings = HuggingFaceEmbeddings(model_name=self.embedding_model)

        vectorstore = Chroma(
            collection_name="documents",
            persist_directory=self.vector_db_dir,
            embedding_function=embeddings
        )

        # Perform similarity search
        results = vectorstore.similarity_search(query, k=top_k)
        return results

    def sixteen_personality_embed(self):
        storage_manager = JSONDataManager(CLEANSED, SIXTEEN_PERSONALITIES_LOC)
        files = storage_manager.get_files()

        for file in files:
            data = storage_manager.load_json(file)
            for key,value in data.items():
                if key == 'ptype':
                    continue
                chunks = self.chunk_text(value)
                vs = self.embed_and_store(chunks)

    def chatGPT_personality_embed(self):
        storage_manager = JSONDataManager(CLEANSED, CHATGPT_PERSONALITIES_LOC)
        files = storage_manager.get_files()

        for file in files:
            data = storage_manager.load_json(file)
            for key,value in data.items():
                chunks = self.chunk_text(value)
                vs = self.embed_and_store(chunks)
