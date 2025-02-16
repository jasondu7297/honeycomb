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
