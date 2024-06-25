from call_tool import (VectorQueryTool,
                       SummaryTool,
                       ResponseHandler,
                       )
def chat(query):

    input_dir = "./docs"
    
    vector_query_tool = VectorQueryTool(input_dir=input_dir)
    vector_tool = vector_query_tool.get_tool()
    
    summary_tool = SummaryTool(nodes=vector_query_tool.nodes)
    summary_tool_instance = summary_tool.get_tool()
    
    response_handler = ResponseHandler()
    
    # i=0
    # while True:
        # user_query = input("Enter your query: ")
    user_query = query
    if user_query.lower() in ["exit", "quit"]:
        print("Ending conversation.")
    response = response_handler.get_response([vector_tool, summary_tool_instance], user_query)
    return response
    # print(f'({i})')
    # print(response)
    # i+=1

# if __name__ == "__main__":
#     main()
