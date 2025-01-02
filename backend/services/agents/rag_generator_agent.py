from core.factories.llm_factory import get_llm
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel, Field
from typing import List

from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate

from langchain_core.prompts import PromptTemplate
from langchain import hub
from services.agents.retrieval_agent import Retrieval

# Pydantic model for input data validation
class GenerationInput(BaseModel):
    context: List[str] = Field(..., description="The list of documents' content for the context")
    question: str = Field(..., description="The question that needs to be answered based on the context")

# Class implementation
class RAGGenerator:
    def __init__(self, is_greeting = False):

        self.is_greeting = is_greeting
        self.llm = get_llm()
      
        message_rag = hub.pull("generate_prompt")
        self.prompt = PromptTemplate.from_template(message_rag)
    

    @staticmethod
    def format_docs(docs: List[str]) -> str:
        """
        Format the list of document contents into a single string.
        Preserves markdown formatting in the documents.
        """
        # Join with double newlines to maintain markdown paragraph spacing
        return "\n\n".join(doc.strip() for doc in docs)

    def invoke(self, input_data: dict):
        """
        Run the RAG generation process.
        """
        context = input_data.get('context', [])
        question = input_data.get('question', '')
        messages = input_data.get('messages', [])[:-1]
        products = input_data.get('products', [])
        gretting_message = input_data.get('gretting_message')
        
        
        if hasattr(context, 'page_content'):
            page_contents = [context.page_content]
        else:
            page_contents = [doc.page_content for doc in context]
            
        formatted_content = self.format_docs(page_contents)

        chain = self.prompt | self.llm

        
        inputs = {
            "context": formatted_content,
            "question": question,
            "chat_history": messages,
            "products": products,
            "gretting_message":gretting_message

        }
        
        return chain.invoke(inputs)
    
    
   
# Example usage
if __name__ == "__main__":
    # Example documents and question
    docs = [
        "This is the content of document 1.",
        "Here is the content of document 2.",
        "The content of document 3 goes here."
    ]
   
    question = "le tarif amanea pro pour un bien de 4 millions et catégorie D"

    # Create an instance of GenerationInput
    input_data = GenerationInput(context=docs, question=question)

    service = Retrieval()
    user_query = "le tarif amanea pro pour un bien de 4 millions et catégorie D"
    documents=service.invoke(user_query)
    


    input_data = {
        "question": question,
        "context": documents,
        
        }

    # Create an instance of RAGGenerator
    rag_generator = RAGGenerator()
    
    # Generate the answer
    result = rag_generator.invoke(input_data)
    
    # Print the generated result
    print(f"Generated Answer: {result}")
