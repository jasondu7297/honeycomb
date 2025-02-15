from Agent import Agent
from langchain.agents import AgentExecutor
from langchain.agents import create_tool_calling_agent
from langgraph.types import Command


class ToolAgent(Agent):
    def run(self, prompt: str) -> None:
        '''
        Processes the given prompt and executes the agent's logic.
        '''
        agent = create_tool_calling_agent(self.model, self.allowed_tools, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=self.allowed_tools, verbose=True)

        response = agent_executor.invoke({'input': prompt})
        return Command(
            goto="supervisor",
            update={"messages": [response]},
        )