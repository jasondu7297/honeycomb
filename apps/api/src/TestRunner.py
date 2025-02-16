from src.conf.ProjectConf import ProjectConf
from src.workflows.Graph import GraphBuilder

class TestRunner:
    def run(self, user_message: str):
        graph_builder = GraphBuilder().build()
        # Stream the output by yielding each chunk instead of printing
        for s in graph_builder.stream(
            {"messages": [("user", user_message)]}, subgraphs=True, config=ProjectConf.state_snapshot_config
        ):
            yield f"{s}\n----\n"  # This yields a string.

if __name__ == "__main__":
    # For standalone testing:
    runner = TestRunner()
    for output in runner.run("Who was the 10th US president?"):
        print(output)
