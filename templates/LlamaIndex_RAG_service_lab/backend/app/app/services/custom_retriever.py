
from typing import List

import asyncio
from app.utils.logging import AppLogger

from llama_index.core import Settings, QueryBundle
from llama_index.core.retrievers import BaseRetriever
from llama_index.core.prompts import PromptTemplate
from llama_index.core.llms import LLM
from llama_index.core.schema import NodeWithScore


logger = AppLogger().get_logger()


class MultiQueriesRetriever(BaseRetriever):
    def __init__(self, base_retriever: BaseRetriever, model: LLM = Settings.llm):
        self.template = PromptTemplate("""You are an AI language model assistant. Your task is to generate Five
    different versions of the given user question to retrieve relevant documents from a vector
    database. By generating multiple perspectives on the user question, your goal is to help
    the user overcome some of the limitations of the distance-based similarity search.
    Provide these alternative questions seperated by newlines.
    Original question: {question}""")
        self._retrievers = [base_retriever]
        self.base_retriever = base_retriever
        self.model = model
    
    def gen_queries(self, query) -> List[str]:
        gen_queries_prompt = self.template.format(question=query)
        prompt = self.template.format(question=query)
        try:
            res = self.model.complete(prompt)
        except Exception as e:
            logger.error(f"Error generating queries: {e}")
            return []
        print(gen_queries_prompt)
        return res.text.split("\n")
    
    async def run_gen_queries(self, generated_queries: List[str]) -> List[NodeWithScore]:
        tasks = list(map(lambda q: self.base_retriever.aretrieve(q), generated_queries))
        res = await asyncio.gather(*tasks)
        return res[0]
    
    def _retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        return list()
    
    async def _aretrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        query = query_bundle.query_str
        generated_queries = self.gen_queries(query)
        query_res = await self.run_gen_queries(generated_queries)
        return query_res

