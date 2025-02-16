from langchain_openai import ChatOpenAI

class ProjectConf:
    '''
    Defines configurations for agentic workflow
    '''
    agent_llm = ChatOpenAI(
        name='openai-llm',
        model="gpt-4o",
        temperature=0,
        timeout=None,
        max_retries=2
    )   # the LLM to be used throughout all agents

    state_snapshot_config = {"configurable": {"thread_id": "1"}}
