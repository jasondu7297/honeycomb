from src.memory.db import knn, write
from src.memory.models import KNNResult, KNNResponse, Document
from src.memory.embeddings import embedding_of_text

# TODO: there's probably some things to do around associating conversations with users, 
# access control, maybe giving an ID to conversations to tie chunks together. We will probably
# save conversation histories wit this DB, so some work will need to go into doing that.

def remember_conversation(conversation: list[str]):
    for chunk in conversation:
        document = Document(text=chunk, embedding=embedding_of_text(chunk))
        write(document)

def get_knn(query: str, k: int) -> KNNResponse:
    knn_results : list[KNNResponse] = []

    base_result = knn(query, k)
    for hit in base_result["hits"]["hits"]:
        knn_results.append(KNNResult(text=hit['_source']['text'], score=hit['_score']))

    return KNNResponse(results=knn_results)
