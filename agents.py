from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
import config

llm = ChatOpenAI(openai_api_key=config.OPENAI_API_KEY, model_name=config.MODEL_NAME, temperature=0.7)

class SimulationAgent:
    def __init__(self, role, scenarios):
        self.role = role
        self.scenarios = scenarios
        self.history = [SystemMessage(content=f"You are a {role} guiding a hospital director through challenges.")]
        self.current_index = 0

    def provide_scenario(self):
        if self.current_index < len(self.scenarios):
            scenario = self.scenarios[self.current_index]["scenario"]
            self.current_index += 1
            return scenario
        return None

    def update_scenario_flow(self, user_response):
        prompt = f"The user, playing as {self.role}, responded: '{user_response}'. Suggest the next challenge."
        response = llm([HumanMessage(content=prompt)])
        self.scenarios.append({"scenario": response.content})

class PerformanceAnalyzingAgent:
    def __init__(self, role):
        self.role = role
        self.history = [SystemMessage(content=f"You analyze how well {role} performed the given scenario .")]
        self.responses = []

    def analyze_response(self, user_response, scenario):
        prompt = f"The user responded: '{user_response}' to the scenario: '{scenario}'. Evaluate the response."
        self.history.append(HumanMessage(content=prompt))
        response = llm(self.history)
        self.history.append(AIMessage(content=response.content))
        self.responses.append(response.content)

    def generate_final_summary(self):
        prompt = f"Based on these responses:\n\n{self.responses}\n\nGive a final performance summary for {self.role}."
        final_analysis = llm([HumanMessage(content=prompt)])
        return final_analysis.content