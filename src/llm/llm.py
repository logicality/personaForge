from transformers import LlamaTokenizer, LlamaForCausalLM, pipeline

class RAGQuery:
    def __init__(self, model_name: str = "meta-llama/Llama-2-7b-chat-hf", device: int = 0):
        """
        Initialize the LLaMA model for RAG.
        Args:
            model_name (str): The Hugging Face model name.
            device (int): Device ID for running the model (e.g., 0 for GPU, -1 for CPU).
        """
        self.tokenizer = LlamaTokenizer.from_pretrained(model_name)
        self.model = LlamaForCausalLM.from_pretrained(model_name, device_map="auto" if device >= 0 else None)
        self.pipeline = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer, device=device)

    def query(self, context: str, question: str, max_length: int = 512) -> str:
        """
        Query the LLaMA model with a context and question.
        Args:
            context (str): The context text retrieved from the vector database.
            question (str): The user question.
            max_length (int): Maximum token length for the generated response.
        Returns:
            str: The generated response from the model.
        """
        prompt = f"""You are a knowledgeable assistant. Use the context below to answer the question thoughtfully:
        Context: {context}
        Question: {question}
        Answer:"""
        
        response = self.pipeline(prompt, max_length=max_length, num_return_sequences=1, do_sample=False)
        return response[0]['generated_text'].strip()
