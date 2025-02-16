from src.workflows.Graph import GraphBuilder

class TestRunner:
    def build(self):
        graph_builder = GraphBuilder().build()

        for s in graph_builder.compile().stream({"messages": [("user", "Can you look at my conversation history and tell me if I've ever asked about Jason?")]}, subgraphs=True):
            print(s)
            print("----")

runner = TestRunner().build()