# personaForge

Project status: In-progress  
Functionality implemented: RAG + LLM. Requires Ollama running on machine. 
- Extract in-depth information about relative topic using chatGPT API or other sources
- Clean/Embed this information
- Get user query
- Embed user query, find relative context from vectorized database
- Feed user query & context to local Ollama model
- Outcome
    + When the query relies on context information, and local model did not have that information in its original training data, model with context performs really well!
    + When the local model did have information related to query in its training data, then both version, context or not, does pretty well, arguibly, not providing context is better here, as context limits scope. This could be fixed though, by providing context as "use as needed" in prompt rather than explicit usage of context for outcome
