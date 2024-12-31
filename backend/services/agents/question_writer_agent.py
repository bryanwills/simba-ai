from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from pydantic import BaseModel, Field
from langchain_core.output_parsers import StrOutputParser

# Load environment variables from .env file
load_dotenv()

if not os.getenv('OPENAI_API_KEY'):
    raise ValueError("OPENAI_API_KEY environment variable not found. Please set it in the .env file.")

# Pydantic model to enforce input formatting
class QuestionInput(BaseModel):
    question: str = Field(..., description="The initial question to be rewritten")
    filenames: list[str] = Field(..., description="List of filenames that contain relevent informations to write suggested questions based on user question")
    products: list[str] = Field(...,description="List of filenames in upper case")

# Class that implements the invocation process
class QuestionRewriter:
    def __init__(self, model_name: str = "gpt-4o", temperature: float = 0):
        # Initialize the LLM with the correct model name
        self.llm = ChatOpenAI(model_name=model_name, temperature=temperature, openai_api_key=os.getenv('OPENAI_API_KEY'), streaming=True)
        
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

    def invoke(self, input_data: QuestionInput) -> str:

        question_list=[]
        filenames=input_data.filenames
        products=input_data.products
        for index, file in enumerate(filenames):
            # file_path = os.path.join("Markdown", file+".md")
            quest = self.extract_questions_from_markdown(file, input_data.question)

            response = {
                "filename": products[index],
                "suggestions" : quest
                }
            question_list.append(response)

        # # Chain the prompt, LLM, and output parser together
        # question_rewriter = self.re_write_prompt | self.llm | self.output_parser
        
        # # Invoke the chain with the formatted input data
        # rewritten_question = question_rewriter.invoke({"question": input_data.question})

        return question_list
    
     
    
    def extract_questions_from_markdown(self, file_path, user_question):
        """
        Extracts questions from a Markdown file using an LLM.

        Args:
            file_path (str): Path to the Markdown file.

        Returns:
            list: A list of extracted questions.
        """

        file_path = file_path.replace("\\", "/")

        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Define the prompt for the LLM
    #     prompt = (
    #             "You are given a question asked by a user. The question is '{user_question}'. "
    #             "First, determine the language used in the question and refer to it as 'lang'. "
    #             "You should then respond in 'lang'. Do not print language or 'lang'. "
    #             "You are an expert user extracting information to quiz people on documentation. "
    #             "Use the user question as a reference to extract tasks. "
    #             "Please analyze the following text and write **exactly three questions** "
    #             "that can be answered solely based on the given text. "
    #             "If the question is not in English, then respond in French:\n\n"
    #         )
        
    #     prompt = """
    #    Question : la question que vous devez répondre
    #    Réflexion : vous devez toujours réfléchir à ce qu'il faut faire
    #    Action : l'action à entreprendre, doit être basée sur {context}
    #    Entrée d'Action : l'entrée à fournir pour l'action
    #    Observation : le résultat de l'action
    #    ... (ce cycle Réflexion/Action/Entrée d'Action/Observation peut se répéter N fois)
    #    Réflexion : je connais maintenant la réponse finale
    #    Instruction : Fournissez uniquement la réponse finale, sans afficher les étapes de réflexion ou d'action intermédiaires.

    #    Commencez !
    #    Contexte : {context}
    #    Question : {user_question}
    
    #    Réponse : (répondez dans la langue de la question, si la question est en Darija marocaine, répondez toujours en Darija.)
       
    #    """
        
        prompt = """
        Vous êtes un expert chargé de répondre aux questions des utilisateurs en analysant un texte donné. Votre rôle est double : fournir une réponse précise à la question posée et, le cas échéant, générer exactement trois questions pertinentes qui peuvent être répondues uniquement à partir du texte fourni. 

        ### Instructions :
        1. **Langue** : Déterminez la langue utilisée dans la question ('lang') et répondez uniquement dans cette langue. Si la question est en Darija marocaine, répondez toujours en Darija.
        2. **Réponse directe** : Fournissez uniquement la réponse finale sans inclure de réflexion, étapes intermédiaires ou actions visibles.
        3. **Création de questions** : Rédigez trois questions exactement, adaptées au contenu du texte fourni, et dans la langue de la question initiale.

        ### Format :
        Question : {user_question}
        Contexte : {content}

        Réponse : 
        """

        questionner_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", prompt),
                (
                    "human",
                    "Voici le fichier markdown de référence : \n\n {content} \n Formulez exactement trois questions basées sur ce texte.",
                ),
            ]
            )
        
        

        # Execute the sequence
        response = (questionner_prompt | self.llm | self.output_parser).invoke({"content": content, "user_question": user_question})


        
        #  Extract the questions from the response
        # Since response is a string, process it directly
        questions = response.strip().split('\n')
            
        return [q for q in questions if q.strip()]

             
            



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
