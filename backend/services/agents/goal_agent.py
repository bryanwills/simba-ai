from langgraph import LangGraph, Agent


# Define an agent that will interact with the user
class GoalAgent(Agent):
    def __init__(self):
        super().__init__()
        self.user_goals = []

    def gather_goals(self):
        # Start a conversation with the user
        print("Hello! I'm here to help you achieve your goals.")
        
        while True:
            goal = input("Please tell me your goal (or type 'done' to finish): ")
            if goal.lower() == 'done':
                break
            self.user_goals.append(goal)
            print(f"Got it! Your current goals are: {self.user_goals}")

    def summarize_goals(self):
        print("\nHere's a summary of your goals:")
        for idx, goal in enumerate(self.user_goals, start=1):
            print(f"{idx}. {goal}")

# Initialize the LangGraph
lang_graph = LangGraph()

# Create an instance of the GoalAgent
goal_agent = GoalAgent()

# Add the agent to the LangGraph
lang_graph.add_agent(goal_agent)

# Start gathering goals
goal_agent.gather_goals()

# Summarize the gathered goals
goal_agent.summarize_goals()