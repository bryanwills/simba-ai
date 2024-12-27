import os
from typing import Any, Dict
from services.agents.greeting_agent import generate_dynamic_greeting, process_greeting
from langchain.schema import Document
from services.agents.retrieval_agent import Retrieval
from services.agents.summary_writer_agent import SummaryWriter,DocumentsInput
from services.agents.rag_generator_agent import RAGGenerator
from services.agents.grader_agent import RetrievalGrader
from services.agents.question_writer_agent import QuestionInput, QuestionRewriter
from services.agents.web_search_agent import TavilySearchTool
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

    # async for chunk in rag_chain.astream({"context": documents, "question": question}):
    #     yield chunk





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
    filenames = state["filenames"]

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
        else:
            print("---GRADE: DOCUMENT NOT RELEVANT---")
            # web_search = "Yes"
            continue
    
    return {"documents": filtered_docs, "question": question, "filenames" : filenames, "web_search": web_search}
    


def question_writer(state):
    """
    Transform the query to produce a better question.

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Updates question key with a re-phrased question
    """

    print("---TRANSFORM QUERY---")
    question = state["question"]
    documents = state["documents"]
    filenames = state["filenames"]
    products = state["products"]

    # Re-write question

    question_to_rewrite = QuestionInput(question=question,filenames=filenames,products=products)

    question_rewriter=QuestionRewriter()
    better_question = question_rewriter.invoke(question_to_rewrite)
    return {"documents": documents, "question": question, "suggestions" : better_question}


def web_search(state):
    """
    Web search based on the re-phrased question.

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Updates documents key with appended web results
    """

    print("---WEB SEARCH---")
    question = state["question"]
    documents = state["documents"]

    # Web search
    web_search_tool=TavilySearchTool()
    docs = web_search_tool.invoke({"query": question})
    web_results = "\n".join([d["content"] for d in docs])
    web_results = Document(page_content=web_results)
    documents.append(web_results)

    return {"documents": documents, "question": question}


### Edges


# def decide_to_generate(state):
#     """
#     Determines whether to generate an answer, or re-generate a question.

#     Args:
#         state (dict): The current graph state

#     Returns:
#         str: Binary decision for next node to call
#     """

#     print("---ASSESS GRADED DOCUMENTS---")
#     state["question"]
#     web_search = state["web_search"]
#     state["documents"]

#     if web_search == "Yes":
#         # All documents have been filtered check_relevance
#         # We will re-generate a new query
#         print(
#             "---DECISION: ALL DOCUMENTS ARE NOT RELEVANT TO QUESTION, TRANSFORM QUERY---"
#         )
#         return "transform_query"
#     else:
#         # We have relevant documents, so generate answer
#         print("---DECISION: GENERATE---")
#         return "generate"



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