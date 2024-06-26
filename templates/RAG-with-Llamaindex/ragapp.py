# Import modules
#What is going under the hood?
import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

import nest_asyncio
nest_asyncio.apply()
import ollama
from llama_index.llms.ollama import Ollama
from pathlib import Path
from llama_index.core import SimpleDirectoryReader
from llama_index.core import VectorStoreIndex, StorageContext, Settings, SummaryIndex, load_index_from_storage
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.tools import QueryEngineTool
from llama_index.core.query_engine.router_query_engine import RouterQueryEngine
from llama_index.core.selectors import LLMSingleSelector
from llama_index.core.schema import IndexNode


import os.path


# Initialize Ollama globally
Settings.llm = Ollama(model="phi3:mini",request_timeout=600,device_map='cuda') #timer set to 600 to prevent timed out error
Settings.embed_model= OllamaEmbedding(model_name="nomic-embed-text")

# check if storage already exists
PERSIST_DIR = "./storage"
if not os.path.exists(PERSIST_DIR):
    # Load the documents
    documents = SimpleDirectoryReader("Research_Papers").load_data()
    # Split the documents
    splitter = SentenceSplitter(chunk_size=1024)
    nodes = splitter.get_nodes_from_documents(documents)
    # Create indices
    summary_index = SummaryIndex(nodes)
    vector_index = VectorStoreIndex(nodes, embed_model=Settings.embed_model)
    
    # Persist indices
    summary_index._storage_context.persist(persist_dir=PERSIST_DIR+r"/summary")
    vector_index._storage_context.persist(persist_dir=PERSIST_DIR+r"/vector")

else:
    # Load the existing indices
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR+r"/summary")
    summary_index = load_index_from_storage(storage_context)
    storage_context1=StorageContext.from_defaults(persist_dir=PERSIST_DIR+r"/vector")
    vector_index = load_index_from_storage(storage_context1)

#Setting the query engine based on the index stored
summary_query_engine = summary_index.as_query_engine(
    response_mode="tree_summarize",
    use_async=True,
)
vector_query_engine = vector_index.as_query_engine()

summary_tool = QueryEngineTool.from_defaults(
        query_engine=summary_query_engine,
        description=(
            "Provide answer to summary related question of the paper"
        ),
    )
    
vector_tool = QueryEngineTool.from_defaults(
    query_engine=vector_query_engine,
    description=(
        "Provide specific answers related to the paper."
        ),
    )
#route queries to appropriate query engine based on the tools
query_engine = RouterQueryEngine(
    selector=LLMSingleSelector.from_defaults(),
    query_engine_tools=[
        summary_tool,
        vector_tool,
    ],
    verbose=True
)

#now query the index
response = query_engine.query("How good Query2CAD performs with GPT-4 in comparison to GPT-3.5?")
print(response)


