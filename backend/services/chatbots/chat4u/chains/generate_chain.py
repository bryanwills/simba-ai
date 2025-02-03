# Chain
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from core.factories.llm_factory import get_llm
from langchain_core.output_parsers import StrOutputParser

#prompt = hub.pull("rlm/rag-prompt")
prompt_template = ChatPromptTemplate.from_template("""
    You are a helpful assistant for Orano.
    Your name is Chat4U.
    You are able to answer questions about the documents in the context.
    You are also able to reason and provide general answers 
    You always respond in French. 
    Question: {question} 
    Context: {context}  
    Chat History: {chat_history}
    Answer: 
""")
llm = get_llm()
generate_chain = prompt_template | llm | StrOutputParser()