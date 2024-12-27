from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv
import os
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate

from langchain_core.prompts import PromptTemplate


# Load environment variables from .env file
load_dotenv()
# Pydantic model for input data validation
class GenerationInput(BaseModel):
    context: List[str] = Field(..., description="The list of documents' content for the context")
    question: str = Field(..., description="The question that needs to be answered based on the context")



# Class implementation
class RAGGenerator:
    def __init__(self, model_name: str = "gpt-4o", temperature: float = 0, is_greeting = False):

        self.is_greeting = is_greeting

      
        message_greeting = """
        Rewrite this greeting message without changing anything.
        {gretting_message}

        """

        message_rag = """
        Tu es un assistant intelligent spécialisé dans les produits et services d'assurance ATLANTASANAD fourni dans les documents.  
        Reponds à la question en proposant des solutions spécifiques et adaptées aux besoins décrits en se basant toujours et uniquement sur les documents fourni sans depassé 200 caracteres.

        Consignes pour structurer la réponse :
        - Répondez dans la langue de la question. Si la question est en Darija marocaine, répondez toujours en Darija.
        - Proposez plusieurs produits adaptés à la situation décrite dans la question.
        - Pour chaque produit, expliquez brièvement son objectif et ses avantages (limitez à 2-3 lignes par produit).
        - Adoptez un ton professionnel et accueillant.
        - Utilisez des puces pour énumérer les produits.
        - Si les informations disponibles sont insuffisantes, indiquez clairement que plus d'informations sont nécessaires.
        - utilise toujours l'historique des conversations pour repondre à la question.
        - La réponse doit obligatoirement contenir le nom du produit d'assurance.


        Contexte : {context}
        Question : {question}
        Historique : {chat_history}
        Produits d'assurance : {products}
        Réponse :
        """

        print(f"flag greeting function RAGGenerator:{is_greeting}")

        # Define the prompt template with the correct variables
        if self.is_greeting:
           
            print(f"promt greeting : {message_greeting}")
            prompt = PromptTemplate.from_template(message_greeting)
        else:
             prompt = PromptTemplate.from_template(message_rag)

        
        # Pull the prompt from the hub
        self.prompt = prompt

        # Initialize the language model
        self.llm = ChatOpenAI(
                            model_name="gpt-4o",
                            temperature=0, 
                            openai_api_key=os.getenv('OPENAI_API_KEY'),
                            streaming=True
                            )

        
        # Output parser
        self.output_parser = StrOutputParser()
        
        # Chain the prompt, LLM, and output parser together
        # self.rag_chain = self.prompt | self.llm | self.output_parser
        # Initialize the conversation chain with correct configuration
        
        

    @staticmethod
    def format_docs(docs: List[str]) -> str:
        """
        Format the list of document contents into a single string.
        """
        return "\n\n".join(docs)

    def invoke(self, input_data: dict):
        """
        Run the RAG generation process.
        """
        context = input_data.get('context', [])
        question = input_data.get('question', '')
        messages = input_data.get('messages', [])[:-1]
        products = input_data.get('products', [])
        gretting_message = input_data.get('gretting_message')
        is_greeting = input_data.get('is_greeting')

        
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
    question = "What information is contained in these documents?"

    # Create an instance of GenerationInput
    input_data = GenerationInput(context=docs, question=question)

    # Create an instance of RAGGenerator
    rag_generator = RAGGenerator()
    
    # Generate the answer
    result = rag_generator.invoke(input_data)
    
    # Print the generated result
    print(f"Generated Answer: {result}")
