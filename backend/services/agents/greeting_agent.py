from typing import List, Tuple
from langchain_openai import ChatOpenAI
from langchain.agents import Tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
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

def compare_to_context(query: str) -> str:
    context = summary_of_documents()
    # Split context into sentences
    sentences = [s.strip() for s in context.split('\n') if s.strip()]
    
    # Find most relevant sentences
    relevant = sorted([(s, similarity_score(query, s)) for s in sentences], 
                     key=lambda x: x[1], reverse=True)[:2]
    
    return "\n".join([s[0] for s in relevant])

def is_greeting(text: str) -> str:
    greetings = {
        'en': ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening'],
        'fr': ['bonjour', 'salut', 'bonsoir', 'coucou'],
        'ar': ['مرحبا', 'السلام عليكم', 'صباح الخير', 'مساء الخير']
    }
    
    text = text.lower()
    for lang_greetings in greetings.values():
        if any(g in text for g in lang_greetings):
            return "True"
    return "False"

def detect_language(text: str) -> str:
    try:
        llm = ChatOpenAI(temperature=0)
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a language detection expert. Respond with great precision to the message. "
                      "If the text is Arabic written in Latin letters (like 'marhaba'), respond with both the Latin and Arabic script versions."),
            ("human", "Detect the language of this text: {text}\n\n"
                     "Respond in this exact JSON format:\n"
                     '{{\n'
                     '    "language": "detected_language",\n'
                     '    "response": "your detailed response"\n'
                     '}}\n')
        ])
        chain = prompt | llm
        language = chain.invoke({"text": text}).content.strip()
        return language
    except Exception as e:
        print(f"Error in detect_language: {str(e)}")
        return 'fr'  # Default to french if detection fails

def summary_of_documents() -> str:
    return """
- LIBERIS Pro est une assurance complète pour les professionnels au Maroc, couvrant les dommages aux biens et les responsabilités liées à leur activité, avec des options personnalisables selon les besoins et le budget
- LIBERIS Carte est une assurance qui protège les assurés contre le vol d'espèces retirées, l'utilisation frauduleuse de moyens de paiement perdus ou volés, et la perte ou le vol de pièces administratives et de clés, avec une couverture mondiale
- LIBERIS Education est un produit d'épargne destiné à constituer un capital pour un enfant bénéficiaire, avec des options de garantie en cas de décès ou d'invalidité du souscripteur, et des versements périodiques gérés par ATLANTASANAD Assurance
- LIBERIS Epargne est un produit d'épargne et de placement qui permet de constituer une épargne par des versements initiaux et périodiques, avec une garantie de capital supplémentaire en cas de décès accidentel, destiné aux personnes physiques titulaires d'un compte au Crédit du Maroc
- LIBERIS Habitation est une assurance qui couvre les biens et responsabilités des propriétaires ou locataires en cas de sinistres tels que l'incendie, le vol, ou les dégâts des eaux, tout en offrant des options supplémentaires pour des besoins spécifiques
- LIBERIS Patrimoine Premium est un produit d'épargne destiné aux clients haut de gamme de la Banque Privée, permettant de faire fructifier un capital initial et des primes complémentaires avec des options de capitalisation ou de distribution, tout en offrant des garanties en cas de décès
- LIBERIS Patrimoine est un produit d'épargne et de placement qui permet de fructifier un capital par le versement d'une prime initiale et de primes complémentaires, avec la possibilité de verser un capital supplémentaire en cas de décès accidentel
- LIBERIS Protection Accident est un produit de prévoyance qui offre une indemnisation en cas d'accident, couvrant le décès, l'invalidité permanente, et les frais médicaux pour l'assuré principal et sa famille, avec une couverture mondiale limitée
- LIBERIS Retraite est un produit d'épargne et de placement qui permet de constituer une épargne retraite par capitalisation, avec des garanties complémentaires en cas de décès ou d'invalidité avant 60 ans, pour les clients du Crédit du Maroc âgés de 18 à 60 ans
- LIBERIS Vie est une assurance prévoyance qui garantit le paiement d'un capital assuré en cas de décès ou d'invalidité absolue et définitive de l'adhérent, destinée aux personnes titulaires d'un compte bancaire au Crédit du Maroc
- LIBERIS LSI est un contrat d'assurance qui couvre les frais d'hospitalisation au Maroc et à l'étranger
"""

# Create tools
tools = [
    Tool(
        name="compare_to_context",
        func=compare_to_context,
        description="Useful for comparing user question to available context and finding relevant information"
    ),
    Tool(
        name="is_greeting",
        func=is_greeting,
        description="Checks if the input text is a greeting"
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

# Message history store
message_store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in message_store:
        message_store[session_id] = InMemoryHistory()
    return message_store[session_id]

# Create conversation prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful assistant that provides information about insurance and savings products. 
    Always respond in the same language as the user's message.
    If the user greets you, respond with a greeting and ask how you can help.
    For product questions, use the provided context to give accurate information.
    Be polite, professional, and concise."""),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}"),
])

# Create base chain
llm = ChatOpenAI(temperature=0.7, model="gpt-4")
chain = prompt | llm

# Add message history
chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history",
    verbose=True
)

def process_message(message: str, thread_id: str = None) -> dict:
    """Process a message using the chain with history"""
    try:
        if thread_id is None:
            thread_id = str(uuid.uuid4())
            
        # Detect language and check if greeting
        language = detect_language(message)
        is_greeting_msg = is_greeting(message) == "True"
        
        if is_greeting_msg:
            # Handle greeting
            greeting_contexts = {
                'english': "User has greeted in English. Respond warmly and ask how you can help with insurance products.",
                'french': "L'utilisateur a salué en français. Répondez chaleureusement et demandez comment vous pouvez aider avec les produits d'assurance.",
                'arabic': "المستخدم حيا بالعربية. رد بدفء واسأل كيف يمكنك المساعدة في منتجات التأمين."
            }
            
            response = chain_with_history.invoke(
                {"question": f"{greeting_contexts.get(language, greeting_contexts['english'])}\nUser message: {message}"},
                config={"configurable": {"session_id": thread_id}}
            )
            
            return {
                "language": language,
                "is_greeting": True,
                "response": response.content,
                "continue_conversation": True
            }
        
        else:
            # For product questions, use context
            context = compare_to_context(message)
            response = chain_with_history.invoke(
                {"question": f"Answer this question based on the following context:\nContext: {context}\nQuestion: {message}"},
                config={"configurable": {"session_id": thread_id}}
            )
            
            return {
                "language": language,
                "is_greeting": False,
                "response": response.content,
                "continue_conversation": False
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
    thread_id = str(uuid.uuid4())
    
    while True:
        message = input("\nYou: ")
        if message.lower() in ['quit', 'exit', 'bye']:
            break
            
        response = process_message(message, thread_id)
        print(f"Bot: {response['response']}")
        
        # If it's not a greeting and we got a proper response, end conversation
        if not response.get('continue_conversation', False):
            break

if __name__ == "__main__":
    # Test individual messages
    # test_messages = [
    #     "Bonjour, pouvez-vous me parler de LIBERIS Carte?",
    #     "Hello, what is LSI insurance?",
    #     "مرحبا، هل يمكنك إخباري عن تأمين LSI؟",
    #     "Hi there!",
    #     "What are the coverage limits for LIBERIS Pro?"
    # ]

    # print("\n=== Testing Individual Messages ===")
    # for message in test_messages:
    #     print(f"\nInput: {message}")
    #     response = process_message(message)
    #     print(f"Response: {json.dumps(response, ensure_ascii=False, indent=2)}")
    
    print("\n=== Testing Interactive Conversation ===")
    handle_conversation()
