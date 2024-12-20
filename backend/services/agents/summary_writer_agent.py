from typing import Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents.base import Document
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from pydantic import BaseModel, Field
from langchain_core.output_parsers import StrOutputParser

# Load environment variables from .env file
load_dotenv()
openai_api_key = os.getenv('AS_OPENAI_API_KEY')

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable not found. Please set it in the .env file.")

# Pydantic model to enforce input formatting
class DocumentsInput(BaseModel):
    documents: list[Document] = Field(..., description="List of documents that need to be summarised into a small paragraph")
    
    

# Class that implements the invocation process
class SummaryWriter:
    def __init__(self, model_name: str = "gpt-4o", temperature: float = 0):
        # Initialize the LLM with the correct model name
        self.llm = ChatOpenAI(model_name=model_name, temperature=temperature, openai_api_key=openai_api_key, streaming=True)
        
       # Prompt setup
        system_message = """Determine the language of the input text as 'lang'. You are a professional writer that converts a list of contents into a concise and comprehensive paragraph.
        Always rewrite the summary in the same language as the input text. If the input is in English, write the summary in English; otherwise, respond in the original language.

        Respond in language 'lang'.
        """
        
        self.write_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_message),
                (
                    "human",
                    "Here is the initial list of documents to summarise: \n\n {documents} \n Formulate an improved summary.",
                ),
            ]
        )
        # Output parser
        self.output_parser = StrOutputParser()

    def invoke(self, input_data: list[DocumentsInput]) -> str:
        # Chain the prompt, LLM, and output parser together
        summary_writer = self.write_prompt | self.llm | self.output_parser
        
        # Invoke the chain with the formatted input data
        written_summary = summary_writer.invoke({"documents": input_data.documents})
        return written_summary

# Example usage
if __name__ == "__main__":

    # documents comming from retriever
    
    # Create instances of Document with their content
    doc0 = Document(page_content="d'épargne au profit de l'enfant bénéficiaire, et ce jusqu'à l'âge limite fixé au contrat et au plus tard à la fin du trimestre au cours duquel l'enfant bénéficiaire atteint 18 ans. () versement égal à la moyenne mensuelle des primes d'épargne versées (à l'exclusion des primes complémentaires) durant les 12 mois ayant précédé le décès, l'IAD ou l'interruption du versement des primes (sous réserve que l'interruption n'ait pas dépassé 12 mois consécutifs). - Le versement au profit de l'enfant bénéficiaire d'une rente éducation trimestrielle, payable jusqu'au terme prévu dans les Conditions Particulières et au plus tard à la fin du trimestre au cours duquel l'enfant bénéficiaire")

    doc1 = Document(page_content="de l'enfant bénéficiaire. - Prorogation possible jusqu'au 25ème anniversaire de l'enfant bénéficiaire et 65ème anniversaire du Souscripteur assuré. NB : la demande de prorogation par le Souscripteur assuré doit être faite 3 mois avant le 18ème anniversaire de l'enfant bénéficiaire. - A défaut de liquidation du contrat à l'échéance fixée aux Conditions Particulières, le capital constitué continuera à être valorisé. Cessation des garanties La garantie facultative « Décès et IAD » cesse d'être acquise au 65ème anniversaire du Souscripteur assuré. Le service des prestations de la garantie décès cesse automatiquement après le décès de l'enfant bénéficiaire. L'épargne constituée à la date du")

    doc2 = Document(page_content="assuré ou la reconnaissance par l'assureur de son état d'IAD. Cible - Personnes physiques titulaires d'un compte auprès du Crédit du Maroc. - Clients ayant des enfants âgés de moins de 18 ans au moment de la souscription. - La souscription à la garantie facultative « Décès et IAD » est ouverte pour toute personne âgée de moins de 60 ans au moment de la souscription. Bénéficiaires - En cas de décès du Souscripteur assuré avant le terme du contrat : l'enfant bénéficiaire. - En cas de décès de l'enfant bénéficiaire avant le terme du contrat : le Souscripteur assuré. - En cas de décès simultané du Souscripteur assuré et de l'enfant bénéficiaire avant le terme du contrat : les")

    doc3 = Document(page_content="1 Fiche Produit LIBERIS Education Univers de Protection : Epargne & Placements Objet de la garantie LIBERIS Education permet de constituer une épargne au profit d'un enfant bénéficiaire, par le versement d'une prime initiale (facultative) et de primes d'épargne périodiques et complémentaires. En cas de décès ou d'invalidité absolue et définitive (IAD) du Souscripteur assuré avant le terme du contrat, la garantie facultative permet : - La continuité du versement des primes d'épargne par ATLANTASANAD Assurance, en lieu et place du Souscripteur assuré. - Le versement d'une rente éducation au profit de l'enfant bénéficiaire, payable trimestriellement à terme échu, à partir du dernier jour du trimestre civil au cours duquel survient le décès du Souscripteur")
    
    docs = [doc0, doc1, doc2, doc3]

    # Create an instance of QuestionInput
    input_data = DocumentsInput(documents=docs)
    
    # Create an instance of QuestionRewriter
    summary_rewriter = SummaryWriter()
    
    # Invoke the rewriter with the input data
    written_summary = summary_rewriter.invoke(input_data)
    
    # Print the improved question
    print(f"Written Summary: {written_summary}")
