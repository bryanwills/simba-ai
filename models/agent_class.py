
from abc import abstractmethod
from typing import Any
from classes.state_class import State
from langchain_openai import ChatOpenAI
from langchain.schema import Document


class BaseAgent(State):
    """
    Abstract base class for all agents in the system.
    Provides common functionality and interface for agent implementations.
    """
    def __init__(self, name: str, model: str = None, server: str = None, temperature: float = 0, 
                 model_endpoint: str = None, stop: str = None):
        """
        Initialize the BaseAgent with common parameters.
        
        :param name: The name to register the agent
        :param model: The name of the language model to use
        :param server: The server hosting the language model
        :param temperature: Controls randomness in model outputs
        :param model_endpoint: Specific endpoint for the model API
        :param stop: Stop sequence for model generation
        """
        self.name = name  # Store the initialized name
        self.model = model
        self.server = server
        self.temperature = temperature
        self.model_endpoint = model_endpoint
        self.stop = stop
        self.llm = self.get_llm()
        self.register()

    def get_llm(self, json_response: bool = False, prompt_caching: bool = True):
        """
        Factory method to create and return the appropriate language model instance.
        :param json_response: Whether the model should return JSON responses
        :param prompt_caching: Whether to use prompt caching
        :return: An instance of the appropriate language model
        """
        if self.server == "openai":
            return ChatOpenAI(
                temperature=self.temperature,
                model=self.model,
                json_response=json_response
            )
        
        else:
            raise ValueError(f"Unsupported server type: {self.server}")

    def register(self):
        """
        Register the agent in the global AgentWorkpad and AgentRegistry using its initialized name.
        Stores the agent's docstring in the AgentRegistry.
        """
        # Extract the docstring from the child class
        agent_docstring = self.__class__.__doc__
        if agent_docstring:
            agent_description = agent_docstring.strip()
        else:
            agent_description = "No description provided."

        # Store the agent's description in the AgentRegistry
      
        print(f"Agent '{self.name}' registered to AgentWorkpad and AgentRegistry.")

    def write_to_workpad(self, response: Any):
        """
        Write the agent's response to the AgentWorkpad under its registered name.
        
        :param response: The response to be written to the AgentWorkpad
        """

        response_document = Document(page_content=response, metadata={"agent": self.name})
        # AgentWorkpad[self.name] = response_document

        
        print(f"Agent '{self.name}' wrote to AgentWorkpad.")

    def read_instructions(self, state: State) -> str:
        """
        Read instructions from the MetaAgent in AgentWorkpad if the agent is not MetaAgent.
        This method can be overridden by subclasses.
        
        :param state: The current state of the agent (default is AgentWorkpad)
        :return: Instructions as a string
        """
        # if self.name != "MetaAgent":
            # Read instructions from MetaAgent's entry in the AgentWorkpad
        try:
            instructions = state.get("meta_agent", "")[-1].page_content
            print(f"\n\n{self.name} read instructions from MetaAgent: {instructions}\n\n", 'green')
        except Exception as e:
            print(f"You must have a meta_agent in your workflow: {e}")
            return ""
        return instructions
        # return ""

    @abstractmethod
    def invoke(self, state: State) -> State:
        """
        Abstract method to invoke the agent's main functionality.
        
        :param state: The current state of the agent (default is AgentWorkpad)
        :return: Updated state after invocation
        """
        pass
