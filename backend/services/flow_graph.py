from langgraph.graph import END, StateGraph, START
from langgraph.checkpoint.memory import MemorySaver
from services.flow_functions import *
from services.classes.state_class import State
from dotenv import load_dotenv
load_dotenv() 
workflow = StateGraph(State)



# Initialize MemorySaver with the configuration directly
memory = MemorySaver()   

# Define the nodes
workflow.add_node("retrieve", retrieve)  # retrieve
workflow.add_node("grade_documents", grade_documents)  # grade documents
workflow.add_node("generate", generate)  # generatae
workflow.add_node("transform_query", transform_query)  # transform_query
# workflow.add_node("web_search_node", web_search)  # web search

# Build graph
workflow.add_edge(START, "retrieve")
workflow.add_edge("retrieve", "grade_documents")
# workflow.add_conditional_edges(
#     "grade_documents",
#     decide_to_generate,
#     {
#         "transform_query": "transform_query",
#         "generate": "generate",
#     },
# )
workflow.add_edge("grade_documents", "generate")
workflow.add_edge("generate", "transform_query")
workflow.add_edge("transform_query", END)




# Compile
graph = workflow.compile(checkpointer=memory)

# Generate and display the graph as an image
# image_bytes = graph.get_graph().draw_mermaid_png()
# image = Image.open(io.BytesIO(image_bytes))

# plt.imshow(image)
# plt.axis('off')
# plt.show()

if __name__ == "__main__":
    graph.invoke({"question": "What is the capital of France?"})