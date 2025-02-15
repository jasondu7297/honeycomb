from Agent import Agent

class SupervisorAgent(Agent):
    def run(prompt: str) -> None:
        '''
        Processes the given prompt and executes the agent's logic.
        '''
        pass
    
    def _create_execution_plan() -> None:
        '''
        Use LLM to create an execution plan that will be converted into a list of Steps (internal use only)
        - For each step, perform RAG to determine agents to be used?
        '''
        pass

    def _select_agent() -> None:
        '''
        Execute the correct agent by returning a Command
        '''
        pass

    def _build_agent_prompt() -> str:
        '''
        Build the prompt for the next agent
        '''
        pass

    