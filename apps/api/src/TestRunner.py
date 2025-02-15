from workflows.Graph import GraphBuilder

class TestRunner:
    def build(self):
        graph_builder = GraphBuilder().build()

        for s in graph_builder.compile().stream({"messages": [("user", "Who was the 10th US president?")]}, subgraphs=True):
            print(s)
            print("----")

runner = TestRunner().build()