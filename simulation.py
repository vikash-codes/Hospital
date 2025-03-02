import random
from agents import SimulationAgent, PerformanceAnalyzingAgent
from scenerio import scenario_bank

class HappyHospitalSimulation:
    def __init__(self):
        self.role, self.scenarios = self.assign_role()
        self.simulation_agent = SimulationAgent(self.role, self.scenarios)
        self.performance_analyzer = PerformanceAnalyzingAgent(self.role)

    def assign_role(self):
        """Randomly assigns a role and its corresponding scenarios."""
        role = random.choice(list(scenario_bank.keys()))
        return role, scenario_bank[role]
