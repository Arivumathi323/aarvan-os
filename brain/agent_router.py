from agents.file_agent import FileAgent
from agents.system_agent import SystemAgent
from agents.memory_agent import MemoryAgent
from agents.browser_agent import BrowserAgent
from agents.app_agent import AppAgent
from agents.calculator_agent import CalculatorAgent
from agents.weather_agent import WeatherAgent
from agents.notes_agent import NotesAgent

class AgentRouter:
    def __init__(self):
        self.file = FileAgent()
        self.system = SystemAgent()
        self.memory = MemoryAgent()
        self.browser = BrowserAgent()
        self.app = AppAgent()
        self.calculator = CalculatorAgent()
        self.weather = WeatherAgent()
        self.notes = NotesAgent()

    def route(self, brain_output: dict) -> str:
        agent = brain_output.get("agent", "chat")
        action = brain_output.get("action", "")
        params = brain_output.get("parameters", {})
        response = brain_output.get("response", "")

        if agent == "file":
            result = self.file.execute(action, params)
        elif agent == "system":
            result = self.system.execute(action, params)
        elif agent == "memory":
            result = self.memory.execute(action, params)
        elif agent == "browser":
            result = self.browser.execute(action, params)
        elif agent == "app":
            result = self.app.execute(action, params)
        elif agent == "calculator":
            result = self.calculator.execute(action, params)
        elif agent == "weather":
            result = self.weather.execute(action, params)
        elif agent == "notes":
            result = self.notes.execute(action, params)
        else:
            result = ""

        return f"{response}\n{result}".strip() if result else response