import os
from typing import Any, Dict
from services.agents.greeting_agent import generate_dynamic_greeting, process_greeting
from langchain.schema import Document
from services.agents.retrieval_agent import Retrieval
from services.agents.rag_generator_agent import RAGGenerator
from services.agents.grader_agent import RetrievalGrader
from services.agents.question_writer_agent import QuestionInput, QuestionRewriter

from langchain.memory import ConversationBufferMemory

def greeting(state):
    print("---GREETING---")
    question = state["question"]
    result = process_greeting(question,"")
    result_response = result.get("response")
    result_is_greeting=result.get("is_greeting")
    print(f"result greeting: {result}")
    print(f"flag greetting function greeting {result_is_greeting}")
    documents = Document(page_content = result_response)

    
    return {"generation": result_response, "documents": documents, "question": question, "filenames" : [],"products":[], "is_greeting":result_is_greeting}

def retrieve(state):
    """
    Retrieve documents

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, documents, that contains retrieved documents
    """
    print("---RETRIEVE---")
    question = state["question"]
    messages = state["messages"] #History of the conversation

    # Retrieval with conversation history
    retriever = Retrieval()
    # Format conversation history into a single string
    conversation_context = "\n".join([f"{msg.content}" for msg in messages])
    # Combine current question with conversation history
    augmented_query = f"Current question: {question}\nConversation history:\n{conversation_context}"
    documents = retriever.invoke(user_query=augmented_query)

    # Extracting page_content from the documents
    filenames = [doc.metadata.get('source') for doc in documents]

    products = [
                os.path.splitext(os.path.basename(doc.metadata.get('source')))[0].replace('_', ' ').upper()
                for doc in documents
            ]


    return {"documents": documents, "question": question, "filenames": filenames, "products": products }

def summary_writer(state):
    """
    Use retrieved documents and write a summary

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, documents, that contains retrieved documents
    """
    print("---SUMMARY WRITER---")
    documents = state["documents"]

    # Summary Writter
    input_data = DocumentsInput(documents=documents)

    writer=SummaryWriter()
    documents = writer.invoke(user_query=input_data)
    return {"documents": documents}



def generate(state):
    """
    Generate answer

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, generation, that contains LLM generation
    """
    print("---GENERATE---")
    question = state["question"]
    documents = state["documents"]
    messages = state["messages"]
    products= state["filenames"]
    is_greeting=state["is_greeting"]
    gretting_message=state["generation"]
    
    print(f"flag is_greeting function flow generare {is_greeting}")
    # RAG generation
    rag_chain = RAGGenerator(is_greeting=is_greeting)
    generation = rag_chain.invoke({"context": documents, "question": question, "messages": messages, "products":products, "gretting_message":gretting_message, "is_greeting":is_greeting} )
    return {"generation": generation}





def grade_documents(state):
    """
    Determines whether the retrieved documents are relevant to the question.

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Updates documents key with only filtered relevant documents
    """

    print("---CHECK DOCUMENT RELEVANCE TO QUESTION---")
    question = state["question"]
    documents = state["documents"]
    # filenames = state["filenames"]
    filenames = []

    # Score each doc
    retrieval_grader=RetrievalGrader()
    filtered_docs = []
    web_search = "No"
    for d in documents:
        score = retrieval_grader.invoke(
            {"question": question, "document": d}
        )
        grade = score.binary_score
        if grade == "yes":
            print("---GRADE: DOCUMENT RELEVANT---")
            filtered_docs.append(d)
            filenames.append(d.metadata.get('source'))
        else:
            print("---GRADE: DOCUMENT NOT RELEVANT---")
            # web_search = "Yes"
            continue
    
    return {"documents": filtered_docs, "question": question, "filenames" : filenames, "web_search": web_search}
    


def question_writer(state):
    """
    Generates follow-up questions based on the AI's response and context.

    Args:
        state (dict): The current graph state containing the question, documents,
                     and generated response

    Returns:
        state (dict): Updates state with follow-up questions that can be asked
                     based on the available context
    """

    print("---TRANSFORM QUERY---")
    question = state["question"]
    documents = state["documents"]
    filenames = state["filenames"]
    products = state["products"]

    # Re-write question

    follow_up_questions_input = QuestionInput(
        question=question,
        filenames=filenames,    
        products=products
    )

    follow_up_questions_rewriter= QuestionRewriter()
    follow_up_questions = follow_up_questions_rewriter.invoke(follow_up_questions_input)
    return {"documents": documents, "question": question, "suggestions" : follow_up_questions}




def decide_is_greeting(state):
    """
    Determines whether to generate an answer, or re-generate a question.

    Args:
        state (dict): The current graph state

    Returns:
        str: Binary decision for next node to call
    """
    is_greeting = state["is_greeting"]
    print(is_greeting)
    if is_greeting:
        return "true"
    else:
        return "false"