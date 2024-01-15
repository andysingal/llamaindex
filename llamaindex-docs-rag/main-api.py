from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os
import pinecone
from llama_index import VectorStoreIndex, ServiceContext
from llama_index.vector_stores import PineconeVectorStore
from llama_index.callbacks import LlamaDebugHandler, CallbackManager
from llama_index.chat_engine.types import ChatMode
from llama_index.postprocessor import SentenceEmbeddingOptimizer
from node_postprocessors.duplicate_postprocessing import (
    DuplicateRemoverNodePostprocessor,
)
import logging

logging.basicConfig(level=logging.DEBUG)

# Inicialização da aplicação FastAPI
app = FastAPI()

# Carregar variáveis de ambiente
load_dotenv()

# Configurar o contexto de serviço e o callback manager
llama_debug = LlamaDebugHandler(print_trace_on_end=True)
callback_manager = CallbackManager(handlers=[llama_debug])
service_context = ServiceContext.from_defaults(callback_manager=callback_manager)


# Função para obter o índice Llama
def get_index() -> VectorStoreIndex:
    pinecone.init(
        api_key=os.environ["PINECONE_API_KEY"],
        environment=os.environ["PINECONE_ENVIRONMENT"],
    )
    index_name = "llamaindex-documentation-helper"
    pinecone_index = pinecone.Index(index_name=index_name)
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
    return VectorStoreIndex.from_vector_store(
        vector_store=vector_store, service_context=service_context
    )


# Inicializar o índice Llama
index = get_index()


# Endpoint /chat
@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    user_message = body.get("message")

    postprocessor = SentenceEmbeddingOptimizer(
        embed_model=service_context.embed_model,
        percentile_cutoff=0.5,
        threshold_cutoff=0.7,
    )
    chat_engine = index.as_chat_engine(
        chat_mode=ChatMode.CONTEXT,
        verbose=True,
        node_postprocessors=[postprocessor, DuplicateRemoverNodePostprocessor()],
    )
    response = chat_engine.chat(message=user_message)
    return JSONResponse(
        {
            "response": response.response,
            # "source_nodes": [node.text for node in response.source_nodes],
        }
    )


# Endpoint de teste
@app.get("/test")
def test():
    return "Test route working!"


# Para rodar o servidor: uvicorn nome_do_seu_arquivo:app --reload


# from llamaindex.node_postprocessor import SentenceEmbeddingOptimizer
# import tensorflow_hub as hub
# from llamaindex.pipeline import LlamaIndexPipeline

# # Carregando o modelo Universal Sentence Encoder pré-treinado
# model = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

# # Criação do otimizador de embedding de sentenças
# embedding_optimizer = SentenceEmbeddingOptimizer(model=model)

# # Criação do pipeline do LlamaIndex
# pipeline = LlamaIndexPipeline(node_postprocessors=[embedding_optimizer])

# # Execução da consulta
# query = "Qual é a capital do Brasil?"
# results = pipeline.search(query)

# # Processamento dos resultados
# for result in results:
#     print(result.text)

# from llamaindex.node_postprocessor import SentenceEmbeddingOptimizer
# from laserembeddings import Laser
# from llamaindex.pipeline import LlamaIndexPipeline

# # Carregando o modelo LASER pré-treinado
# model = Laser()

# # Criação do otimizador de embedding de sentenças
# embedding_optimizer = SentenceEmbeddingOptimizer(model=model)

# # Criação do pipeline do LlamaIndex
# pipeline = LlamaIndexPipeline(node_postprocessors=[embedding_optimizer])

# # Execução da consulta
# query = "Qual é a capital do Brasil?"
# results = pipeline.search(query)

# # Processamento dos resultados
# for result in results:
#     print(result.text)

# from llamaindex.node_postprocessor import SentenceEmbeddingOptimizer
# from sentence_transformers import SentenceTransformer
# from llamaindex.pipeline import LlamaIndexPipeline

# # Carregando o modelo Sentence-BERT pré-treinado
# model = SentenceTransformer('bert-base-nli-mean-tokens')

# # Criação do otimizador de embedding de sentenças
# embedding_optimizer = SentenceEmbeddingOptimizer(model=model)

# # Criação do pipeline do LlamaIndex
# pipeline = LlamaIndexPipeline(node_postprocessors=[embedding_optimizer])

# # Execução da consulta
# query = "Qual é a capital do Brasil?"
# results = pipeline.search(query)

# # Processamento dos resultados
# for result in results:
#     print(result.text)

# fast text
# from llamaindex.node_postprocessor import SentenceEmbeddingOptimizer
# import fasttext
# from llamaindex.pipeline import LlamaIndexPipeline

# # Carregando o modelo fastText pré-treinado
# model = fasttext.load_model('path/to/fasttext/model.bin')

# # Criação do otimizador de embedding de sentenças
# embedding_optimizer = SentenceEmbeddingOptimizer(model=model)

# # Criação do pipeline do LlamaIndex
# pipeline = LlamaIndexPipeline(node_postprocessors=[embedding_optimizer])

# # Execução da consulta
# query = "Qual é a capital do Brasil?"
# results = pipeline.search(query)

# # Processamento dos resultados
# for result in results:
#     print(result.text)
