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
        max_retries=2,
        api_key='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',
    )   # the LLM to be used throughout all agents

    state_snapshot_config = {"configurable": {"thread_id": "1"}}
