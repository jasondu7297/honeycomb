import re
from typing import Dict, List, Any

def extract_graph_data(snapshot_str: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Extracts message data from the snapshot string and returns a dictionary
    with nodes and edges for graph visualization.
    
    Each node represents a message (HumanMessage, AIMessage, ToolMessage) with:
      - id: the message id
      - label: the message content
      - type: the message type
      
    Edges are created sequentially from one message to the next.
    """
    # Regular expression pattern to capture:
    #  - The message type (HumanMessage, AIMessage, or ToolMessage)
    #  - The content (everything between "content='" and the next single quote)
    #  - The first occurrence of an id value (the first id='...') after the content.
    pattern = re.compile(
        r"(HumanMessage|AIMessage|ToolMessage)\(content='(.*?)'.*?id='(.*?)'",
        re.DOTALL
    )

    # Find all matches in the snapshot string.
    matches = pattern.findall(snapshot_str)
    
    nodes = []
    for msg_type, content, msg_id in matches:
        nodes.append({
            "id": msg_id,
            "label": content,
            "type": msg_type,
        })
    
    # Create edges by linking each message to the next one.
    edges = []
    for i in range(1, len(nodes)):
        edges.append({
            "source": nodes[i - 1]["id"],
            "target": nodes[i]["id"]
        })

    return {"nodes": nodes, "edges": edges}


# --- Example usage ---
if __name__ == "__main__":
    test_snapshots = ("[StateSnapshot(values={'messages': [HumanMessage(content='Who was the 10th US president?', "
                      "additional_kwargs={}, response_metadata={}, id='b1a585f0-866d-42f2-9216-a8693e94ea84'), "
                      "AIMessage(content='', additional_kwargs={'tool_calls': [{'id': 'call_YMbF7OkWWH2AFQb5VedTKBY7', "
                      "'function': {'arguments': '{}', 'name': 'transfer_to_gsearchagent'}, 'type': 'function'}], "
                      "'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 14, 'prompt_tokens': 1011, "
                      "'total_tokens': 1025, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, "
                      "'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, "
                      "'cached_tokens': 0}}, 'model_name': 'gpt-4o-2024-08-06', 'system_fingerprint': 'fp_523b9b6e5f', "
                      "'finish_reason': 'tool_calls', 'logprobs': None}, name='supervisor', id='run-0b75c81a-cad3-424f-afd1-a407860c62f1-0', "
                      "tool_calls=[{'name': 'transfer_to_gsearchagent', 'args': {}, 'id': 'call_YMbF7OkWWH2AFQb5VedTKBY7', "
                      "'type': 'tool_call'}], usage_metadata={'input_tokens': 1011, 'output_tokens': 14, 'total_tokens': 1025, "
                      "'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}), "
                      "ToolMessage(content='Successfully transferred to GSearchAgent', name='transfer_to_gsearchagent', "
                      "id='444b7002-2f15-4c02-89a2-93ece54df238', tool_call_id='call_YMbF7OkWWH2AFQb5VedTKBY7'), "
                      "AIMessage(content='The 10th President of the United States was John Tyler. He served from 1841 to 1845.', "
                      "additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 26, "
                      "'prompt_tokens': 96, 'total_tokens': 122, 'completion_tokens_details': {'accepted_prediction_tokens': 0, "
                      "'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': "
                      "{'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-2024-08-06', 'system_fingerprint': "
                      "'fp_ff092ab25e', 'finish_reason': 'stop', 'logprobs': None}, name='GSearchAgent', id='run-643d10b3-2a23-4c6e-9d63-751e62685f53-0', "
                      "usage_metadata={'input_tokens': 96, 'output_tokens': 26, 'total_tokens': 122, 'input_token_details': "
                      "{'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}), "
                      "AIMessage(content='Transferring back to supervisor', additional_kwargs={}, response_metadata={}, "
                      "name='GSearchAgent', id='2e842837-2dfb-42a4-a968-a1cab66533df', tool_calls=[{'name': "
                      "'transfer_back_to_supervisor', 'args': {}, 'id': 'a1780a61-b190-4b29-8b7b-ea7b4ec494c1', 'type': "
                      "'tool_call'}]), ToolMessage(content='Successfully transferred back to supervisor', "
                      "name='transfer_back_to_supervisor', id='2ecaee32-8cfd-460f-9a12-74d069214010', tool_call_id='a1780a61-b190-4b29-8b7b-ea7b4ec494c1'), "
                      "AIMessage(content='The 10th President of the United States was John Tyler, who served from 1841 to 1845.', "
                      "additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 26, "
                      "'prompt_tokens': 1120, 'total_tokens': 1146, 'completion_tokens_details': {'accepted_prediction_tokens': 0, "
                      "'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': "
                      "{'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-2024-08-06', 'system_fingerprint': "
                      "'fp_523b9b6e5f', 'finish_reason': 'stop', 'logprobs': None}, name='supervisor', "
                      "id='run-43497ffa-1c02-41e1-a8a7-6972bef70e35-0', usage_metadata={'input_tokens': 1120, 'output_tokens': 26, "
                      "'total_tokens': 1146, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': "
                      "{'audio': 0, 'reasoning': 0}})]}, next=(), config={'configurable': {'thread_id': '1', "
                      "'checkpoint_ns': '', 'checkpoint_id': '1efec06f-9830-6b34-8003-44c253a3e2aa'}}, metadata={...}]")
    
    graph_data = extract_graph_data(test_snapshots)
    print(graph_data)
