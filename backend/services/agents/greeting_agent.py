# from typing import List, Tuple
# from langchain_openai import ChatOpenAI
# from langchain.agents import Tool
# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain_core.messages import HumanMessage, AIMessage
# from langchain_core.runnables.history import RunnableWithMessageHistory
# from langchain_core.chat_history import BaseChatMessageHistory
# from langchain_core.output_parsers import StrOutputParser
# from langchain.prompts import PromptTemplate
# from functools import lru_cache

# from langdetect import detect
# from difflib import SequenceMatcher
# from dotenv import load_dotenv
# import json
# import uuid
# import os


# # Load environment variables from .env file
# load_dotenv()


# def similarity_score(a: str, b: str) -> float:
#     return SequenceMatcher(None, a.lower(), b.lower()).ratio()

# # def compare_to_context(query: str) -> str:
# #     context = summary_of_documents()
# #     # Split context into sentences
# #     sentences = [s.strip() for s in context.split('\n') if s.strip()]
    
# #     # Find most relevant sentences
# #     relevant = sorted([(s, similarity_score(query, s)) for s in sentences], 
# #                      key=lambda x: x[1], reverse=True)[:2]
    
# #     return "\n".join([s[0] for s in relevant])

#     # Template pour identifier si un message est une salutation
# greeting_detection_prompt = PromptTemplate.from_template("""
#     Tu es un assistant qui identifie si une question est une salutation (greeting).  
#     Voici ce que tu dois faire :  
#     - Réponds uniquement par "GREETING" si la question est une salutation comme "bonjour", "salut", "hello", "salam" ou toute autre forme de salutation.  
#     - Réponds uniquement par "NOT_GREETING" si ce n'est pas une salutation.

#     Question : {question}
#     Réponse :
#     """)
# llm = ChatOpenAI(model_name="gpt-4o", temperature=0)

# greeting_chain = greeting_detection_prompt | llm | StrOutputParser()

# def detect_language(question: str) -> str:
#     """
#     Détecte la langue de la question pour informer le modèle.
#     """
#     llm = ChatOpenAI(model_name="gpt-4o", temperature=0.0)
#     language_detection_prompt = ChatPromptTemplate.from_messages([
#         ("system", "Tu es un détecteur de langue. Indique simplement 'DAR' si la langue est Darija marocaine,'AR' si la langue est Arabe, 'FR' pour français, et 'OTHER' pour toute autre langue."),
#         ("human", "Voici le texte : {question}. Quelle est la langue ? Réponds uniquement par 'DAR', 'FR' ou 'OTHER'.")
#     ])
#     chain = language_detection_prompt | llm | StrOutputParser()
#     detected_language = chain.invoke({"question": question}).strip()
#     return detected_language

# def generate_dynamic_greeting(question: str) -> str:
#     """

#     Génère une réponse dynamique aux salutations, en respectant strictement la langue détectée.
#     """
#     llm = ChatOpenAI(model_name="gpt-4o", temperature=0.3)

#     # Détecter la langue
#     detected_language = detect_language(question)
#     print(f"Langue détectée : {detected_language}")

#     # Choisir un prompt selon la langue détectée
#     #if detected_language == "DAR":
#     if detected_language in ["DAR", "AR"]:
#         system_message = (
#             "Tu es un assistant d'assurance d'ATLANTASANAD ASSURANCES. "
#             "Réponds STRICTEMENT en Darija marocaine, de manière chaleureuse, polie et professionnelle. "
#             "N'utilise JAMAIS d'autres langues comme le français ou l'anglais ou l'arabe. Reste simple et naturel."
#         )
#         #system_message = "Réponds chaleureusement en Darija marocaine, de façon simple et professionnelle, pour un assistant d'assurance pour les produits ATLANTASANAD ASSURANCES."
#     elif detected_language == "FR":
#         system_message = "Réponds chaleureusement et professionnellement en français pour un assistant d'assurance pour les produits ATLANTASANAD ASSURANCES."
#     else:
#         system_message = "Réponds dans la langue originale détectée, de façon simple et professionnelle."

#     # Prompt avec sélection de langue
#     greeting_prompt = ChatPromptTemplate.from_messages([
#         ("system", system_message),
#         ("human", "Question : {question}\nRéponse :")
#     ])
#     chain = greeting_prompt | llm | StrOutputParser()

#     try:
#         response = chain.invoke({"question": question}).strip()
#         print(f"Dynamic Greeting Response: {response}")
#         return response
#     except Exception as e:
#         print(f"Erreur : {e}")
#         return "Wa alaykum salam! Chno n9der n3awnk bach twsl l'information d'assurance?"


# @lru_cache(maxsize=20)  # Cache 20 résultats récents
# def generate_dynamic_greeting_cached(question: str) -> str:
#     """
#     Génère une réponse dynamique aux salutations avec mise en cache pour éviter les appels redondants.
#     """
#     print("Appel au modèle LLM pour générer la salutation...")
#     return generate_dynamic_greeting(question)  

# # def summary_of_documents() -> str:
# #     return """
# # - LIBERIS Pro est une assurance complète pour les professionnels au Maroc, couvrant les dommages aux biens et les responsabilités liées à leur activité, avec des options personnalisables selon les besoins et le budget
# # - LIBERIS Carte est une assurance qui protège les assurés contre le vol d'espèces retirées, l'utilisation frauduleuse de moyens de paiement perdus ou volés, et la perte ou le vol de pièces administratives et de clés, avec une couverture mondiale
# # - LIBERIS Education est un produit d'épargne destiné à constituer un capital pour un enfant bénéficiaire, avec des options de garantie en cas de décès ou d'invalidité du souscripteur, et des versements périodiques gérés par ATLANTASANAD Assurance
# # - LIBERIS Epargne est un produit d'épargne et de placement qui permet de constituer une épargne par des versements initiaux et périodiques, avec une garantie de capital supplémentaire en cas de décès accidentel, destiné aux personnes physiques titulaires d'un compte au Crédit du Maroc
# # - LIBERIS Habitation est une assurance qui couvre les biens et responsabilités des propriétaires ou locataires en cas de sinistres tels que l'incendie, le vol, ou les dégâts des eaux, tout en offrant des options supplémentaires pour des besoins spécifiques
# # - LIBERIS Patrimoine Premium est un produit d'épargne destiné aux clients haut de gamme de la Banque Privée, permettant de faire fructifier un capital initial et des primes complémentaires avec des options de capitalisation ou de distribution, tout en offrant des garanties en cas de décès
# # - LIBERIS Patrimoine est un produit d'épargne et de placement qui permet de fructifier un capital par le versement d'une prime initiale et de primes complémentaires, avec la possibilité de verser un capital supplémentaire en cas de décès accidentel
# # - LIBERIS Protection Accident est un produit de prévoyance qui offre une indemnisation en cas d'accident, couvrant le décès, l'invalidité permanente, et les frais médicaux pour l'assuré principal et sa famille, avec une couverture mondiale limitée
# # - LIBERIS Retraite est un produit d'épargne et de placement qui permet de constituer une épargne retraite par capitalisation, avec des garanties complémentaires en cas de décès ou d'invalidité avant 60 ans, pour les clients du Crédit du Maroc âgés de 18 à 60 ans
# # - LIBERIS Vie est une assurance prévoyance qui garantit le paiement d'un capital assuré en cas de décès ou d'invalidité absolue et définitive de l'adhérent, destinée aux personnes titulaires d'un compte bancaire au Crédit du Maroc
# # - LIBERIS LSI est un contrat d'assurance qui couvre les frais d'hospitalisation au Maroc et à l'étranger
# # """

# # Create tools
# tools = [
#     # Tool(
#     #     name="compare_to_context",
#     #     func=compare_to_context,
#     #     description="Useful for comparing user question to available context and finding relevant information"
#     # ),
#     Tool(
#         name="is_greeting",
#         func= generate_dynamic_greeting,
#         description="Checks if the input text is a greeting"
#     ),
#     Tool(
#         name="language_detect",
#         func=detect_language,
#         description="Detects the language of the input text"
#     )
# ]

# # Create an in-memory message history store
# class InMemoryHistory(BaseChatMessageHistory):
#     def __init__(self):
#         self.messages = []
    
#     def add_message(self, message):
#         self.messages.append(message)
    
#     def clear(self):
#         self.messages = []

# # Message history store
# message_store = {}

# def get_session_history(session_id: str) -> BaseChatMessageHistory:
#     if session_id not in message_store:
#         message_store[session_id] = InMemoryHistory()
#     return message_store[session_id]

# # Create conversation prompt
# prompt = ChatPromptTemplate.from_messages([
#     ("system", """You are a helpful assistant that provides information about insurance and savings products. 
#     Always respond in the same language as the user's message.
#     If the user greets you, respond with a greeting and ask how you can help.
#     For product questions, use the provided context to give accurate information.
#     Be polite, professional, and concise."""),
#     MessagesPlaceholder(variable_name="history"),
#     ("human", "{question}"),
# ])

# # Create base chain
# llm = ChatOpenAI(temperature=0.7, model="gpt-4")
# chain = prompt | llm

# # Add message history
# chain_with_history = RunnableWithMessageHistory(
#     chain,
#     get_session_history,
#     input_messages_key="question",
#     history_messages_key="history",
#     verbose=True
# )

# def process_message(message: str, thread_id: str = None) -> dict:
#     """Process a message using the chain with history"""
#     try:
#         if thread_id is None:
#             thread_id = str(uuid.uuid4())
            
#         # Detect language and check if greeting
#         language = detect_language(message)
#         is_greeting_msg = generate_dynamic_greeting(message) == "True"
        
#         if is_greeting_msg:
#             # Handle greeting
#             greeting_contexts = {
#                 'english': "User has greeted in English. Respond warmly and ask how you can help with insurance products.",
#                 'french': "L'utilisateur a salué en français. Répondez chaleureusement et demandez comment vous pouvez aider avec les produits d'assurance.",
#                 'arabic': "المستخدم حيا بالعربية. رد بدفء واسأل كيف يمكنك المساعدة في منتجات التأمين."
#             }
            
#             response = chain_with_history.invoke(
#                 {"question": f"{greeting_contexts.get(language, greeting_contexts['english'])}\nUser message: {message}"},
#                 config={"configurable": {"session_id": thread_id}}
#             )
            
#             return {
#                 "language": language,
#                 "is_greeting": True,
#                 "response": response.content,
#                 "continue_conversation": True
#             }
        
#         else:
#             # For product questions, use context
#             # context = compare_to_context(message)
#             # response = chain_with_history.invoke(
#             #     {"question": f"Answer this question based on the following context:\nContext: {context}\nQuestion: {message}"},
#             #     config={"configurable": {"session_id": thread_id}}
#             # )
            
#             return {
#                 "language": language,
#                 "is_greeting": False,
#                 "response": response.content,
#                 "continue_conversation": False
#             }
            
#     except Exception as e:
#         print(f"Error in process_message: {str(e)}")
#         return {
#             "language": language,
#             "is_greeting": False,
#             "response": "I apologize, but I encountered an error. Please try again.",
#             "continue_conversation": False
#         }

# def handle_conversation():
#     thread_id = str(uuid.uuid4())
    
#     while True:
#         message = input("\nYou: ")
#         if message.lower() in ['quit', 'exit', 'bye']:
#             break
            
#         response = process_message(message, thread_id)
#         print(f"Bot: {response['response']}")
        
#         # If it's not a greeting and we got a proper response, end conversation
#         if not response.get('continue_conversation', False):
#             break

# if __name__ == "__main__":
#     # Test individual messages
#     # test_messages = [
#     #     "Bonjour, pouvez-vous me parler de LIBERIS Carte?",
#     #     "Hello, what is LSI insurance?",
#     #     "مرحبا، هل يمكنك إخباري عن تأمين LSI؟",
#     #     "Hi there!",
#     #     "What are the coverage limits for LIBERIS Pro?"
#     # ]

#     # print("\n=== Testing Individual Messages ===")
#     # for message in test_messages:
#     #     print(f"\nInput: {message}")
#     #     response = process_message(message)
#     #     print(f"Response: {json.dumps(response, ensure_ascii=False, indent=2)}")
    
#     print("\n=== Testing Interactive Conversation ===")
#     handle_conversation()



from typing import List, Tuple
from langchain.chat_models import ChatOpenAI
from langchain.agents import Tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate
from functools import lru_cache

from langdetect import detect
from difflib import SequenceMatcher
from dotenv import load_dotenv
import json
import uuid
import os

# Load environment variables from .env file
load_dotenv()

def similarity_score(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

# Prompt for detecting if a message is a greeting
greeting_detection_prompt = PromptTemplate.from_template("""
    Tu es un assistant qui identifie si une question est une salutation (greeting).  
    Voici ce que tu dois faire :  
    - Réponds uniquement par "GREETING" si la question est une salutation comme "bonjour", "salut", "hello", "salam" ou toute autre forme de salutation.  
    - Réponds uniquement par "NOT_GREETING" si ce n'est pas une salutation.

    Question : {question}
    Réponse :
""")

# Model used for greeting detection
llm_detection = ChatOpenAI(model_name="gpt-4", temperature=0)
greeting_chain = greeting_detection_prompt | llm_detection | StrOutputParser()

def is_greeting(question: str) -> bool:
    """
    Return True if the question is a greeting, False otherwise.
    """
    result = greeting_chain.invoke({"question": question}).strip()
    return result == "GREETING"

def detect_language(question: str) -> str:
    """
    Détecte la langue de la question pour informer le modèle.
    Renvoie 'DAR' si la langue est Darija marocaine,
    'AR' pour Arabe,
    'FR' pour Français,
    'OTHER' sinon.
    """
    llm_lang = ChatOpenAI(model_name="gpt-4", temperature=0.0)
    language_detection_prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "Tu es un détecteur de langue. Indique simplement 'DAR' si la langue est Darija marocaine,'AR' si la langue est Arabe, "
            "'FR' pour français, et 'OTHER' pour toute autre langue."
        ),
        (
            "human",
            "Voici le texte : {question}. Quelle est la langue ? "
            "Réponds uniquement par 'DAR', 'AR', 'FR' ou 'OTHER'."
        )
    ])
    chain = language_detection_prompt | llm_lang | StrOutputParser()
    detected_language = chain.invoke({"question": question}).strip()
    return detected_language

@lru_cache(maxsize=20)
def generate_dynamic_greeting(question: str) -> str:
    """
    Génère une réponse dynamique aux salutations, en respectant strictement la langue détectée.
    """
    llm = ChatOpenAI(model_name="gpt-4", temperature=0.3)

    # Détecter la langue
    detected_language = detect_language(question)
    print(f"Langue détectée : {detected_language}")

    # Choisir un prompt selon la langue détectée
    if detected_language in ["DAR", "AR"]:
        system_message = (
            "Tu es un assistant d'assurance d'ATLANTASANAD ASSURANCES. "
            "Réponds STRICTEMENT en Darija marocaine, de manière chaleureuse, polie et professionnelle. "
            "N'utilise JAMAIS d'autres langues comme le français ou l'anglais ou l'arabe classique. Reste simple et naturel."
        )
    elif detected_language == "FR":
        system_message = (
            "Tu es un assistant d'assurance d'ATLANTASANAD ASSURANCES. "
            "Réponds chaleureusement et professionnellement en français."
        )
    else:
        system_message = (
            "Tu es un assistant d'assurance d'ATLANTASANAD ASSURANCES. "
            "Réponds dans la langue de l'utilisateur, de façon simple et professionnelle."
        )

    # Prompt pour la réponse
    greeting_prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("human", "Question : {question}\nRéponse :")
    ])
    chain = greeting_prompt | llm | StrOutputParser()

    try:
        response = chain.invoke({"question": question}).strip()
        print(f"Dynamic Greeting Response: {response}")
        return response
    except Exception as e:
        print(f"Erreur : {e}")
        return (
            "Wa alaykum salam! Chno n9der n3awnk bach twsl l'information d'assurance?"
            " (Message d'erreur par défaut)"
        )

# Tools (optionally used by an agent, if needed)
tools = [
    Tool(
        name="is_greeting",
        func=generate_dynamic_greeting,
        description="Generate a dynamic greeting message"
    ),
    Tool(
        name="language_detect",
        func=detect_language,
        description="Detects the language of the input text"
    )
]

# Create an in-memory message history store
class InMemoryHistory(BaseChatMessageHistory):
    def __init__(self):
        self.messages = []
    
    def add_message(self, message):
        self.messages.append(message)
    
    def clear(self):
        self.messages = []

# Dictionary to store chat histories by session
message_store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in message_store:
        message_store[session_id] = InMemoryHistory()
    return message_store[session_id]

# Conversation prompt
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a helpful assistant that provides information about insurance and savings products.
    Always respond in the same language as the user's message.
    If the user greets you, respond with a greeting and ask how you can help.
    Be polite, professional, and concise."""
    ),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}"),
])

# LLM chain with history
llm_main = ChatOpenAI(model_name="gpt-4", temperature=0.7)
chain = prompt | llm_main
chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history",
    verbose=True
)

def process_greeting(message: str, thread_id: str = None) -> dict:
    """
    Process a message using the chain with history, detect language, and see if it's a greeting.
    """
    # Define a default in case an exception occurs before setting it
    language = "unknown"
    try:
        if thread_id is None:
            thread_id = str(uuid.uuid4())
        
        # 1. Detect language
        language = detect_language(message)

        # 2. Check if it is a greeting
        greeting_detected = is_greeting(message)

        if greeting_detected:
            # The user just greeted us; generate a dynamic greeting in the correct language.
            # Then pass that greeting into the chain if you want to keep the conversation going.
            greeting_response = generate_dynamic_greeting(message)

            # Optionally, you could store greeting_response or do something else with it
            # For demonstration, we'll just return the dynamic greeting.
            return {
                "language": language,
                "is_greeting": True,
                "response": greeting_response,
                "continue_conversation": True
            }
        else:
            # 3. Not a greeting => proceed with your normal chain logic
            response = chain_with_history.invoke(
                {"question": message},
                config={"configurable": {"session_id": thread_id}}
            )
            return {
                "language": language,
                "is_greeting": False,
                "response": response.content,
                "continue_conversation": True
            }

    except Exception as e:
        print(f"Error in process_message: {str(e)}")
        return {
            "language": language,
            "is_greeting": False,
            "response": "I apologize, but I encountered an error. Please try again.",
            "continue_conversation": False
        }

def handle_conversation():
    """
    Simple interactive loop for testing in the console.
    """
    thread_id = str(uuid.uuid4())
    
    while True:
        message = input("\nYou: ")
        if message.lower() in ['quit', 'exit', 'bye']:
            print("Bot: Goodbye!")
            break
            
        response_data = process_greeting(message, thread_id)
        print(f"Bot: {response_data['response']}")
        
        # If you want to end after the first non-greeting response:
        if not response_data.get('continue_conversation', False):
            break

if __name__ == "__main__":
    print("\n=== Testing Interactive Conversation ===")
    handle_conversation()
