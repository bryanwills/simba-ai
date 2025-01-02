from langchain_openai import ChatOpenAI
from langchain.agents import Tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate
from core.config import settings
from difflib import SequenceMatcher
import uuid
from langchain import hub

from dotenv import load_dotenv
load_dotenv()


def similarity_score(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

# Prompt for detecting if a message is a greeting
greeting_detection_prompt = hub.pull("greeting_detection_prompt:258c6a52")

# Model used for greeting detection
llm_detection = ChatOpenAI(model_name="gpt-4o", temperature=0)
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
    llm_lang = ChatOpenAI(model_name="gpt-4o", temperature=0)
    language_detection_prompt  = hub.pull("language_detection_prompt")
    
    chain = language_detection_prompt | llm_lang | StrOutputParser()
    detected_language = chain.invoke({"question": question}).strip()
    return detected_language

def generate_dynamic_greeting(question: str) -> str:
    """
    Génère une réponse dynamique aux salutations, en respectant strictement la langue détectée.
    """
    llm = ChatOpenAI(model_name="gpt-4o", temperature=0.3)

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
llm_main = ChatOpenAI(model_name="gpt-4o", temperature=0.7)
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
