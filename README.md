# NewsIntel-LLM
Semantic search application, facilitating the transformation of news URLs into vector representations via word embeddings, stored in a FAISS Index. Utilized OpenAI’s API to deliver precise responses to equity research analysts.

## Features

- Load URLs or upload text files containing URLs to fetch article content.
- Process article content through LangChain's UnstructuredURL Loader
- Construct an embedding vector using OpenAI's embeddings and leverage FAISS, a powerful similarity search library, to enable swift and effective retrieval of relevant information
- Interact with the LLM's (Chatgpt) by inputting queries and receiving answers along with source URLs.
