from google.adk.agents import SequentialAgent
from .sub_agents import DelegateAgent, OutputAgent
class ChatAgentOrchestrator:
    def __init__(self):
        # Root Agent
        self.root_agent = SequentialAgent(
            name='ChatAgentPipeline',
            sub_agents=[DelegateAgent,OutputAgent],
            description="An pipeline that converts a user_query into well strcutred response",
        )

