from config import ProjectConf
from src.workflows.Graph import GraphBuilder

from typing import Any

class Runner:
    """
    A production-ready runner that streams output from graph_builder.
    """
    def __init__(self, config: dict[str, Any] = ProjectConf.state_snapshot_config):
        self.config = config
        self.graph = GraphBuilder.build()

    def run(self, user_message: str):
        print("[INFO] Running production runner with message:", user_message)

        # Stream the output by yielding each chunk
        for chunk in self.graph.stream(
            {"messages": [("user", user_message)]}, subgraphs=True, config=self.config
        ):
            yield f"{chunk}\n----\n"
