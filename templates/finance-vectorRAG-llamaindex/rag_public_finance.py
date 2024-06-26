# -*- coding: utf-8 -*-
# Retrieval-Augmented Generation (RAG) Chatbot for Finance

"""Access to files"""

import os
import markdown
path = os.path.join("data", "documents")
persist_dir = os.path.join("data", "storage")


"""Large Language Model"""

import torch
from llama_index.llms.groq import Groq

prompt="""
You are a Public Finance assistant and advisor, speciallized in tax administration, your role is to provide clear, precise and detailed but concise responses to the user questions.
If you don't know how to respond, just say it, don't try to create or imagine false information.
Answer as fluently as possible, try to keep a natural conversation.
Use markdown syntax to enhance the look and readability of your answers and jump lines to keep the conversation clear.
This are few exemples of a good comversation:
==== example 1 ====
User:What are the most important technologies to develop for tax administration by the end of 2024 ?

Assistant: **According to the provided context, the most important technologies to develop for tax administration by the end of 2024 include:**

1. **Artificial Intelligence for Automation**: Implement AI-powered systems to automate tasks, such as processing tax returns, identifying errors, and reducing manual intervention.
2. **Blockchain for Secure Data Storage**: Utilize blockchain technology to securely store tax-related data, ensuring enhanced data integrity and transparency.
3. **Cloud-Based Platforms**: Migrate tax administration systems to cloud-based platforms, enabling scalability, flexibility, and cost-effective operations.
4. **Natural Language Processing**: Integrate NLP to improve customer service, providing intuitive and personalized support to taxpayers.
5. **Predictive Analytics**: Leverage predictive analytics to identify potential tax evasion, detect anomalies, and optimize tax collection.

These technologies are considered crucial for improving tax administration efficiency, effectiveness, and responsiveness to taxpayers.
==== example 2 ====
User question:How to tackle the inflation ?

Assistant: **Addressing Inflation and Fiscal Policy**

In the context of the provided sources, addressing inflation requires a multi-faceted approach that involves fiscal policy, monetary policy, and structural reforms. According to the Fiscal Monitor (April 2024), fiscal policies should focus on directing innovation, promoting productivity growth, and ensuring the overall gains are fairly and widely shared.

To tackle inflation, the report suggests implementing fiscal policies that:

1. **Reduce fiscal deficits**: Gradually reduce fiscal deficits to stabilize debt and boost fiscal space.
2. **Promote innovation**: Encourage innovation, particularly in green sectors, to drive productivity growth and reduce emissions.
3. **Enhance tax capacity**: Strengthen institutional capacity and tax systems to mobilize revenue and reduce fiscal gaps.
4. **Implement structural reforms**: Pursue structural reforms to improve productivity, labor market flexibility, and competitiveness.

In addition, the report highlights the importance of international cooperation, institutional capacity building, and medium-term reform plans to address the challenges posed by inflation.

**Key Takeaways**

1. Fiscal policy should prioritize innovation, productivity growth, and fairness to address inflation.
2. Implementing fiscal policies that reduce deficits, promote innovation, and enhance tax capacity is crucial.
3. Structural reforms and international cooperation are essential to address the root causes of inflation.

**References**

* Fiscal Monitor (April 2024)
* Benitez and others (2023)
* IMF (2023b)
"""

# Select a model from Groq API: "llama3-70b-8192" "llama3-8b-8192" "mixtral-8x7b-32768" "Gemma-7b-it"
model = "llama3-8b-8192"
llm = Groq(
    model=model,
    api_key=os.environ.get("GROQ_KEY"),
    temperature=0.8,
    system_prompt=prompt,
)
print("LLM loaded successfully")


"""Embedding model"""

from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# Load the embedding model
embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-base-en-v1.5", 
    device="cuda" if torch.cuda.is_available() else "cpu",
    trust_remote_code=True,
    cache_folder="cache",
)


"""RAG Settings"""

from groq import Groq as Groq_API
from llama_index.core import Settings
from llama_index.core.node_parser import SentenceSplitter, SemanticSplitterNodeParser

client = Groq_API(api_key=os.environ.get('GROQ_KEY'))

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext, load_index_from_storage, get_response_synthesizer
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine


""" Vector Database """

# Cector database class to store the index
class VectorDatabase:
    # Intialize the vector database from the existing index
    def __init__(self):
        # Llama-index settings
        Settings.llm = llm
        Settings.embed_model = embed_model
        Settings.node_parser = SentenceSplitter(
            chunk_size=2048,
            chunk_overlap=256,
        )
        Settings.num_output = 256
        Settings.context_window = 4096 # Maximum size of the input query
        self.settings = Settings
        if not os.path.exists(persist_dir):
            # Load the documents and create the index
            documents = SimpleDirectoryReader(path).load_data()
            nodes = Settings.node_parser.get_nodes_from_documents(documents) # split documents into chunks depending
            index = VectorStoreIndex(nodes)
            # Store it for later
            index.storage_context.persist(persist_dir=persist_dir)
        # Load the index from the storage
        storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
        self.index = load_index_from_storage(storage_context)
        print("Index loaded successfully")

    # Reset the index
    def reset(self):
        # Delete the existing index
        if os.path.exists(persist_dir):
            os.remove(persist_dir)
        # Load the documents and create the index
        self.__init__()
    

""" RAG Chatbot """

# RAG chatbot class to respond to the user queries
class RAG:
    # Initialize the RAG chatbot
    def __init__(self, vector_database, chat_history="", messages=[]):
        self.vector_database = vector_database
        # Configure retriever
        retriever = VectorIndexRetriever(
            index=vector_database.index,
            similarity_top_k=5,
            verbose=False,
        )
        # Configure response synthesizer
        response_synthesizer = get_response_synthesizer(
            response_mode="refine",
        )
        # Assemble query engine
        self.query_engine = RetrieverQueryEngine(
            retriever=retriever,
            response_synthesizer=response_synthesizer,
        )
        # Memory of the chatbot
        self.chat_history = chat_history
        self.messages = messages
        print("RAG chatbot loaded successfully")
    
    
    # Switching model
    def switch_model(self, model):
        self.vector_database.__init__(llm=Groq(model=model, api_key=os.environ.get('GROQ_KEY')))
        self.__init__(self.vector_database, self.chat_history, self.messages)
        print("Switched to", self.vector_database.settings.llm.model)

    # Chat history summarization
    def summarize(self):
        history_summarizer = client.chat.completions.create(
            messages=[{
                "role": "system",
                "content": "Just summarize the given conversation, it will be used as context for the ongoing conversation. Focus on the user informations and the last assistant message. Do NOT continue the conversation. Write precise and concise summary.\n\nConversation: " + str(self.chat_history),
            }], model="llama3-8b-8192", temperature=0.8)
        self.chat_history = history_summarizer.choices[-1].message.content
    
    # Respond to the user query
    def respond(self, query):
        final_query = "======\nConversation history: " + self.chat_history + "\n======\n\n" + "User question:" + query + "\n\nAssistant: "
        raw_response = self.query_engine.query(final_query)
        response = markdown.markdown(str(raw_response))
        self.chat_history += "\n\nUser:" + query
        self.chat_history += "\n\nAssistant:" + str(raw_response)
        self.summarize()
        self.messages.append({"user": "User", "text": query})
        self.messages.append({"user": "Assistant", "text": response})

    # Reset the chat history
    def reset_history(self):
        self.chat_history = ""
        self.messages = []