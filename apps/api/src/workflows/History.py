from typing import Any, Union
from langchain_core.messages import HumanMessage

from conf.ProjectConf import ProjectConf
from Graph import GraphBuilder

class WorkflowHistory:
    _conf = ProjectConf.state_snapshot_config
    
    @classmethod
    def get_history(cls) -> str:
        graph = GraphBuilder.get_graph()
        return str(graph.get_state_history(cls._conf))

    @classmethod
    def update(cls, checkpoint_id: int, new_prompt: str) -> Union[dict[str, Any], Any]:
        graph = GraphBuilder.get_graph()
        for state in graph.get_state_history(cls._conf):
            if state.config['configurable'] and state.config['configurable']['checkpoint_id'] == checkpoint_id:
                state.values['messages'][-1] = HumanMessage(new_prompt) # assuming last message will be human message
        
        cls.replay(checkpoint_id)

    def _replay(checkpoint_id: int) -> Union[dict[str, Any], Any]:
        # set the checkpoint id to be used for replay
        update_conf = ProjectConf.state_snapshot_config
        update_conf['configurable']['checkpoint_id'] = checkpoint_id

        graph = GraphBuilder.get_graph()
        return graph.invoke(None, config=update_conf)
