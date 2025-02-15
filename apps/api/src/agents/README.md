# Agents

Agents use an LLM as a reasoning engine to decide what actions to take and execute those action. Some agents will be equipped with external sources or tools to enhance its performance. To add a new agent, please adhere to the following steps:

Below, we will walkthrough the steps of adding a new agent, `FakeAgent`. 
1. Create a new derived class of `Agent` for `FakeAgents` :
```
from AgentRegistry import AgentRegistry

@AgentRegistry.register
class FakeAgent(Agent):
    def build(self) -> CompiledStateGraph:
        pass
```

2. Construct a `StateGraph` in `build`
```
from AgentRegistry import AgentRegistry

@AgentRegistry.register
class FakeAgent(Agent):
    def build(self) -> CompiledStateGraph:
        graph = StateGraph(state_schema)

        # Define the two nodes we will cycle between
        workflow.add_node(...)
```

3. `build` must return a `CompiledStateGraph` by calling `.compile`