from typing import Any, Union

from config import ProjectConf
from src.workflows.Graph import GraphBuilder
from langgraph.types import StateSnapshot

class WorkflowHistory:
    _conf = ProjectConf.state_snapshot_config
    
    @classmethod
    def get_history(cls) -> str:
        graph = GraphBuilder.get_graph()
        return str(list(graph.get_state_history(cls._conf)))

    @classmethod
    def update(cls, checkpoint_id: str, new_prompt: str) -> Union[dict[str, Any], Any]:
        graph = GraphBuilder.get_graph()
        print("Updating history...")
        print(checkpoint_id)
        print(new_prompt)
        for state in graph.get_state_history(cls._conf):
            if state.config['configurable'] and state.config['configurable']['checkpoint_id'] == checkpoint_id:
                state.values['messages'] = [new_prompt]
                graph.update_state(state.config, {'messages': 'messages'})

                return graph.stream({'messages': [new_prompt]}, state.config, stream_mode="values")

            print("Invalid checkpoint_id, should not reach this point")
            return None # Invalid checkpoint_id, should not reach this point