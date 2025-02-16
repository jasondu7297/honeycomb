# apps/api/src/TestRunner.py
if __name__ == "__main__":
    # For standalone testing:
    runner = TestRunner()
    for output in runner.run("Who was the 10th US president?"):
        print(output)
        for s in graph_builder.compile().stream({"messages": [("user", "Can you look at my conversation history and tell me if I've ever asked about Jason?")]}, subgraphs=True):
            print(s)
            print("----")

runner = TestRunner().build()
