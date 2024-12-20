from langgraph.graph import Graph



class QueryUnderstandingNode:
    def run(self, user_query):
        # Analyze the query (could involve NLP techniques like entity recognition)
        refined_query = self.refine_query(user_query)
        return refined_query

    def refine_query(self, query):
        # Example: Lowercase the query and remove stop words
        # You could also use NLP models here for better understanding
        return query.lower()


class DocumentRetrievalNode:
    def __init__(self, rag_tool):
        self.rag_tool = rag_tool

    def run(self, refined_query):
        # Fetch documents using the RAG tool
        retrieved_docs = self.rag_tool._run(query_text=refined_query)
        return retrieved_docs


class AdaptiveResponseNode:
    def __init__(self, llm_model):
        self.llm_model = llm_model

    def run(self, user_query, retrieved_docs):
        # Concatenate document content for LLM response generation
        doc_texts = " ".join([doc['text'] for doc in retrieved_docs])
        
        # Generate a response using the LLM model, including the query and relevant documents
        response = self.llm_model.generate_response(user_query, doc_texts)
        return response


class FeedbackLoopNode:
    def run(self, user_query, generated_response):
        # Ask the user if they want to refine the query based on the response
        user_feedback = self.get_user_feedback(generated_response)
        
        # If the user wants to refine, adjust the query and run retrieval again
        if user_feedback == 'refine':
            refined_query = self.get_refined_query(user_query, generated_response)
            return refined_query
        else:
            return generated_response

    def get_user_feedback(self, response):
        # In a real system, you would ask the user for feedback
        # For this example, assume the user always wants to refine
        return 'refine'

    def get_refined_query(self, user_query, response):
        # Modify the query based on the generated response
        return user_query + " additional clarification"



# Define the graph with nodes for each step
class AdaptiveRAGGraph(Graph):
    def __init__(self, rag_tool, llm_model):
        super().__init__()
        self.query_node = QueryUnderstandingNode()
        self.retrieval_node = DocumentRetrievalNode(rag_tool)
        self.response_node = AdaptiveResponseNode(llm_model)
        self.feedback_node = FeedbackLoopNode()

    def run(self, user_query):
        # Step 1: Refine the query
        refined_query = self.query_node.run(user_query)
        
        # Step 2: Retrieve relevant documents
        retrieved_docs = self.retrieval_node.run(refined_query)
        
        # Step 3: Generate adaptive response
        response = self.response_node.run(user_query, retrieved_docs)
        
        # Step 4: Handle feedback loop for query refinement
        final_response = self.feedback_node.run(user_query, response)
        
        return final_response
