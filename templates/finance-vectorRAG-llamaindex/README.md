# finance-vectorRAG-llamaindex
Finance assistant implemented with VectorRAG.

The **Large Language Models (LLMs)** used are from the **Groq API**, the Embedding model run locally with the `transformers` library.
The **Vector Retrieval Augmented Generation (RAG)** model is implemented with the `llama-index` library.

## Installation

The next command will build the docker image and run it on port 5000.
To run properly the docker need to have a GROQ API key in the environment variable `GROQ_KEY`.

```bash

docker build -t finance-vector-rag-llamaindex .
docker run -it -p 5000:5000 -e GROQ_KEY=<your_groq_key> finance-vector-rag-llamaindex

```