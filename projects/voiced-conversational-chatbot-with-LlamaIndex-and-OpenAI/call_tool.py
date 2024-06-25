import os
from helpers import get_openai_api_key
OPENAI_API_KEY = get_openai_api_key()

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, SummaryIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.vector_stores import MetadataFilters, FilterCondition
from llama_index.core.tools import FunctionTool, QueryEngineTool
from llama_index.llms.openai import OpenAI
from typing import List

class VectorQueryTool:
    def __init__(self, input_dir: str, chunk_size: int = 1024):
        self.documents = self.load_all_pdfs(input_dir)
        self.splitter = SentenceSplitter(chunk_size=chunk_size)
        self.nodes = self.splitter.get_nodes_from_documents(self.documents)
        self.vector_index = VectorStoreIndex(self.nodes)
    
    def load_all_pdfs(self, directory: str):
        pdf_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.pdf')]
        return SimpleDirectoryReader(input_files=pdf_files).load_data()
    
    def vector_query(self, query: str, page_numbers: List[str]) -> str:
        """Perform a vector search over an index."""
        metadata_dicts = [{"key": "page_label", "value": p} for p in page_numbers]
        query_engine = self.vector_index.as_query_engine(
            similarity_top_k=2,
            filters=MetadataFilters.from_dicts(metadata_dicts, condition=FilterCondition.OR)
        )
        response = query_engine.query(query)
        return response
    
    def get_tool(self):
        return FunctionTool.from_defaults(name="vector_tool", fn=self.vector_query)


class SummaryTool:
    def __init__(self, nodes):
        self.summary_index = SummaryIndex(nodes)
        self.summary_query_engine = self.summary_index.as_query_engine(
            response_mode="tree_summarize",
            use_async=True,
        )
    
    def get_tool(self):
        return QueryEngineTool.from_defaults(
            name="summary_tool",
            query_engine=self.summary_query_engine,
            description="Useful if you want to get a summary of the provided document!"
        )


class ResponseHandler:
    def __init__(self, model="gpt-3.5-turbo", temperature=0):
        self.llm = OpenAI(model=model, temperature=temperature)
        self.conversation_history = []
    
    def add_to_history(self, user_query: str, response: str):
        self.conversation_history.append({"user_query": user_query, "response": response})
    
    def summarize_history(self):
        if len(self.conversation_history) > 10:  # Summarize if history is long
            conversation_summary = " ".join([f"User: {entry['user_query']} Bot: {entry['response']}" for entry in self.conversation_history])
            summary_query = f"Summarize the following conversation: {conversation_summary}"
            summary_response = self.llm.predict(summary_query)
            self.conversation_history = [{"user_query": "Summary", "response": summary_response}]
    
    def get_response(self, tools: List, query: str):
        try:
            response = self.llm.predict_and_call(tools, query, verbose=True)
            response_text = self.inspect_response(response)
            self.add_to_history(query, response_text)
            self.summarize_history()
            return response_text
        except ValueError as e:
            if "Expected at least one tool call" in str(e):
                return "No relevant tool calls were made for this query."
            else:
                raise e
    
    @staticmethod
    def inspect_response(response):
        attributes = [attr for attr in dir(response) if not attr.startswith("__")]
        for attr in attributes:
            try:
                value = getattr(response, attr)
                if not callable(value):
                    if attr == "response":
                        return f'Response: {value}'
            except AttributeError:
                print(f"Could not access attribute: {attr}")

