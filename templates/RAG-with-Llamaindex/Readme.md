

## Answer given by the LLM
The performance of Query2CAD using GPT-4 as a language model surpasses that achieved with GPT-3.5 when it comes to easy and medium difficulty levels, registering accurarances of 95.23% and 70%, respectively. Convers contrastingly, the use of GPT-3.5-Turbo resulted in lower accuracy rates on these same difficulty levels - an ease level performance at 85.71% and medium/hard levels at 35% and 37.5%. This comparison demonstrates a significant improvement when using GPT-4 over GPT-3.5 for the Query2CAD system in generating correct 3D CAD models as per user queries, particularly on easier and somewhat challenging tasks.

### Though the LLM answered the question correctly, it also gave nonsense answer unrelated to the question. 
### Also it takes a long time for inference. So, the reply comes very late. So, the request time out has been increased to 600s. But still sometimes, LLM is not able to infer the answer. Prompt Engineering might help.
### Finding specific answer using Vector_Query_engine is less GPU intensive than summary_query engine.
### The RouterQueryEngine() was up to the mark in selecting the required query_engine as per the question.

