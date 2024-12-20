from chromadb import Documents
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from .retrieval_agent import Retrieval
from pydantic import BaseModel, Field


# Data model for grading
class GradeDocuments(BaseModel):
    """Binary score for relevance check on retrieved documents."""
    binary_score: str = Field(description="Documents are relevant to the question, 'yes' or 'no'.")

class RetrievalGrader:
    def __init__(self):
        # Set the USER_AGENT environment variable to avoid the warning
        os.environ["USER_AGENT"] = "MyPythonAgent/1.0"

        # Load environment variables from .env file
        load_dotenv()
        self.openai_api_key = os.getenv('AS_OPENAI_API_KEY')

        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable not found. Please set it in the .env file.")

        # Initialize the LLM
        self.llm = ChatOpenAI(model_name="gpt-4o", temperature=0, openai_api_key=self.openai_api_key, streaming=True)

        # Setup the structured output grader
        self.structured_llm_grader = self.llm.bind_tools([GradeDocuments])

        # Set up the grading prompt
        self.grade_prompt = self._create_grade_prompt()

        # Chain the prompt with the grader
        self.retrieval_grader = self.grade_prompt | self.structured_llm_grader

        

    def _create_grade_prompt(self):
        """
        Create the grading prompt used for assessing the relevance of documents.
        """
        system = """You are a grader assessing the relevance of a retrieved document to a user question.
        If the document contains keyword(s) or semantic meaning related to the question, grade it as relevant.
        Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question."""

        return ChatPromptTemplate.from_messages(
            [
                ("system", system),
                ("human", "Retrieved document:\n\n{document}\n\nUser question: {question}")
            ]
        )

    def invoke(self, input_data: dict):
        """
        Invoke the grading process on the provided documents based on the question.
        Args:
            input_data (dict): A dictionary containing 'question' (str) and 'documents' (list of Documents).
        Returns:
            list: A list of dictionaries with each document's content and its binary score.
        """
        # Extract the question and documents from input_data
        question = input_data.get("question")
        doc = input_data.get("document")

        if not question or not doc:
            raise ValueError("Both 'question' and 'documents' must be provided in the input data.")

       
        if doc:
            grading_result = self.retrieval_grader.invoke({"question": question, "document": doc})

            # Extract the binary_score from the grading result
            tool_calls = grading_result.additional_kwargs.get('tool_calls', [])
            if tool_calls:
                binary_score = eval(tool_calls[0]['function']['arguments']).get('binary_score', 'no')

               
                return GradeDocuments(binary_score=binary_score)

            
            else:
                print("No tool calls found in grading result.")
        else:
            print("No page content found for this document.")

        




# Example usage
def usage():
    """
        Retrieve documents and grade their relevance to the given question.
       """
    # question = "andi bent ou bghit nedman liha moustakbal dialha"
    question = "j'ai une fille et je souhaite assurer son avenir"

    # Retrieve documents
    retriever = Retrieval()
    docs = retriever.invoke(user_query=question)
    if not docs or len(docs) < 2:
        raise ValueError("Expected at least two documents retrieved for grading.")
    

    grader = RetrievalGrader()
    
    grading_result = grader.invoke({"question": question, "document": docs})


    binary_score_result = grading_result
    text_result = docs[:1000]
    print(f"Binary score: #{binary_score_result}# for document : {text_result} \n" )


# usage()