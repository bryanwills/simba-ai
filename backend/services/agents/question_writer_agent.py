from core.factories.llm_factory import get_llm
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
<<<<<<< HEAD
=======
from langchain_core.output_parsers import StrOutputParser
>>>>>>> 9ce89b7 (module)

# Pydantic model to enforce input formatting
class QuestionInput(BaseModel):
    user_question: str = Field(..., description="the question asked by the user")
    ai_response: str = Field(..., description="the response of the AI")
    context: str = Field(..., description="the context of the AI response")

# Class that implements the invocation process
class QuestionRewriter:
    def __init__(self):
        # Initialize the LLM with the correct model name
        self.llm = get_llm()
<<<<<<< HEAD
=======
        
        # Prompt setup
        system_message = """You are a question re-writer that converts an input question to a better version optimized for web search.
        Always rewrite the question in the same language as the input text. If the input is in English, rewrite the question in English outherwise do not respond in English.
        
        Always give 3 questions with different contexts
        
        """
        
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_message),
                (
                    "human",
                    "Here is the initial question: \n\n {question} \n Formulate an improved question.",
                ),
            ]
        )
        # Output parser
        self.output_parser = StrOutputParser()
>>>>>>> 9ce89b7 (module)

        self.prompt  = ChatPromptTemplate.from_messages([
            ("system", 
                """
                    Vous êtes un expert chargé de répondre aux questions des utilisateurs en analysant un texte donné. 
                    Votre rôle est de générer exactement trois questions pertinentes qui peuvent être répondues uniquement à partir du texte fourni.

                    Instructions :
                    1. Analysez le contexte fourni
                    2. Générez exactement trois questions pertinentes
                    3. Retournez uniquement les questions, une par ligne

                    Question : {user_question}
                    AI response : {ai_response}
                """
             
             )
            (
                "human",
                "Voici le fichier markdown de référence : \n\n {context} \n Formulez exactement trois questions basées sur ce texte.",
            ),
        ])

        
    def invoke(self, input_data: QuestionInput) -> str:

        chain = self.prompt | self.llm | self.output_parser
        response = chain.invoke({
            "context": input_data.context,  
            "user_question": input_data.user_question,
            "ai_response": input_data.ai_response
        })
        questions = [q.strip() for q in response.split('\n') if q.strip()][:3]

        return questions
        

# Example usage
if __name__ == "__main__":

    # text comming from grader agent
    text="""
        1 Fiche Produit LIBERIS Education Univers de Protection : Epargne & Placements Objet de la garantie LIBERIS Education permet de constituer une épargne au profit d'un enfant bénéficiaire, par le versement d'une prime initiale (facultative) et de primes d'épargne périodiques et complémentaires. En cas de décès ou d'invalidité absolue et définitive (IAD) du Souscripteur assuré avant le terme du contrat, la garantie facultative permet : - La continuité du versement des primes d'épargne par ATLANTASANAD Assurance, en lieu et place du Souscripteur assuré. - Le versement d'une rente éducation au profit de l'enfant bénéficiaire, payable trimestriellement à terme échu, à partir du dernier jour du trimestre civil au cours duquel survient le décès du Souscripteur     
        Binary score: yes for document : d'épargne au profit de l'enfant bénéficiaire, et ce jusqu'à l'âge limite fixé au contrat et au plus tard à la fin du trimestre au cours duquel l'enfant bénéficiaire atteint 18 ans. () versement égal à la moyenne mensuelle des primes d'épargne versées (à l'exclusion des primes complémentaires) durant les 12 mois ayant précédé le décès, l'IAD ou l'interruption du versement des primes (sous réserve que l'interruption n'ait pas dépassé 12 mois consécutifs). - Le versement au profit de l'enfant bénéficiaire d'une rente éducation trimestrielle, payable jusqu'au terme prévu dans les Conditions Particulières et au plus tard à la fin du trimestre au cours duquel l'enfant bénéficiaire        
        """
    # Create an instance of QuestionInput
    input_data = QuestionInput(question=text)
    
    # Create an instance of QuestionRewriter
    question_rewriter = QuestionRewriter()
    
    # Invoke the rewriter with the input data
    rewritten_question = question_rewriter.invoke(input_data)
    
    # Print the improved question
    print(f"Rewritten Question: {rewritten_question}")
