import os
from langchain.schema import Document
from services.agents.retrieval_agent import Retrieval
from services.agents.summary_writer_agent import SummaryWriter,DocumentsInput
from services.agents.rag_generator_agent import RAGGenerator
from services.agents.grader_agent import RetrievalGrader
from services.agents.question_writer_agent import QuestionInput, QuestionRewriter
from services.agents.web_search_agent import TavilySearchTool


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

    # Retrieval
    retriever=Retrieval()
    documents = retriever.invoke(user_query=question)

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

    # RAG generation
    rag_chain = RAGGenerator()
    generation = rag_chain.invoke({"context": documents, "question": question})
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
    


def transform_query(state):
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


def decide_to_generate(state):
    """
    Determines whether to generate an answer, or re-generate a question.

    Args:
        state (dict): The current graph state

    Returns:
        str: Binary decision for next node to call
    """

    print("---ASSESS GRADED DOCUMENTS---")
    state["question"]
    web_search = state["web_search"]
    state["documents"]

    if web_search == "Yes":
        # All documents have been filtered check_relevance
        # We will re-generate a new query
        print(
            "---DECISION: ALL DOCUMENTS ARE NOT RELEVANT TO QUESTION, TRANSFORM QUERY---"
        )
        return "transform_query"
    else:
        # We have relevant documents, so generate answer
        print("---DECISION: GENERATE---")
        return "generate"