from dotenv import load_dotenv
import os
import pinecone
from llama_index import VectorStoreIndex, ServiceContext
from llama_index.vector_stores import PineconeVectorStore
from llama_index.callbacks import LlamaDebugHandler, CallbackManager
from llama_index.chat_engine.types import ChatMode
import streamlit as st
from llama_index.postprocessor import SentenceEmbeddingOptimizer
from node_postprocessors.duplicate_postprocessing import (
    DuplicateRemoverNodePostprocessor,
)


load_dotenv()

print("*** Streamlit llamaindex doc helper")

llama_debug = LlamaDebugHandler(print_trace_on_end=True)
callback_manager = CallbackManager(handlers=[llama_debug])
service_context = ServiceContext.from_defaults(callback_manager=callback_manager)


@st.cache_resource(show_spinner=False)
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


index = get_index()

if "chat_engine" not in st.session_state.keys():
    # é possivel utilizar embeddings models open source como Sentence-BERT, Universal Sentence Encoder e LASER, no final do artigo contem alguns exemplos
    postprocessor = SentenceEmbeddingOptimizer(
        embed_model=service_context.embed_model,
        percentile_cutoff=0.5,
        threshold_cutoff=0.7,
    )

    st.session_state.chat_engine = index.as_chat_engine(
        chat_mode=ChatMode.CONTEXT,
        verbose=True,
        node_postprocessors=[postprocessor, DuplicateRemoverNodePostprocessor()],
    )

st.set_page_config(
    page_title="Chat with llamaindex docs, powered by LlamaIndex",
    page_icon="🙀",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)

st.title("Chat with llamaindex docs 🙀")

if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Ask me a question about LlamaIndex's open source python library",
        }
    ]

if prompt := st.chat_input("Your question"):
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.chat(message=prompt)
            st.write(response.response)
            nodes = [node for node in response.source_nodes]
            # for col, node, i in zip(st.columns(len(nodes)), nodes, range(len(nodes))):
            # with col:
            # st.header(f"Source Node {i+1}: score={node.score}")
            # st.write(node.text)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message)


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
