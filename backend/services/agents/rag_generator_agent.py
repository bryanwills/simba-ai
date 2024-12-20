from langchain import hub
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
openai_api_key = os.getenv('AS_OPENAI_API_KEY')
# Pydantic model for input data validation
class GenerationInput(BaseModel):
    context: List[str] = Field(..., description="The list of documents' content for the context")
    question: str = Field(..., description="The question that needs to be answered based on the context")

# Class implementation
class RAGGenerator:
    def __init__(self, model_name: str = "gpt-4o", temperature: float = 0):
        
        
        

        # Pull the prompt from the hub
        self.prompt = hub.pull("rlm/rag-prompt")

        # Initialize the language model
        self.llm = ChatOpenAI(model_name=model_name, temperature=temperature, openai_api_key=openai_api_key, streaming=True)

        
        # Output parser
        self.output_parser = StrOutputParser()
        
        # Chain the prompt, LLM, and output parser together
        self.rag_chain = self.prompt | self.llm | self.output_parser

    @staticmethod
    def format_docs(docs: List[str]) -> str:
        """
        Format the list of document contents into a single string.
        """
        return "\n\n".join(docs)

    def invoke(self, input_data: dict) -> str:
        """
        Run the RAG generation process.
        """
        context=input_data.get('context')
        question=input_data.get('question')
        # Format the documents
       
        # Extracting page_content from the documents
        page_contents = [doc.page_content for doc in context]

        # Formatting the contents
        formatted_content = self.format_docs(page_contents)

        
        # Invoke the RAG chain
        generation = self.rag_chain.invoke({"context": formatted_content, "question": question})
        
        return generation

# Example usage
if __name__ == "__main__":
    # Example documents and question
    docs = [
        "This is the content of document 1.",
        "Here is the content of document 2.",
        "The content of document 3 goes here."
    ]
    question = "What information is contained in these documents?"

    # Create an instance of GenerationInput
    input_data = GenerationInput(context=docs, question=question)

    # Create an instance of RAGGenerator
    rag_generator = RAGGenerator()
    
    # Generate the answer
    result = rag_generator.invoke(input_data)
    
    # Print the generated result
    print(f"Generated Answer: {result}")
