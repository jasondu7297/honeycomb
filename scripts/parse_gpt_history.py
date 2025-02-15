"""
This script parses an exported ChatGPT [conversations.json], generates embeddings from it,
and generates the required files to visualize it with Wizmap.

requirements:
------------
wizmap
numpy<2.0
umap-learn
sentence-transformers
"""

import json
import wizmap

from pathlib import Path
from sentence_transformers import SentenceTransformer
from umap import UMAP

######################################################
# CONSTANTS
######################################################

file = "conversations.json"
N_DIMENSIONS = 384

######################################################
# DATA INGESTION
######################################################

data = json.loads(Path(file).open().read())

######################################################
# EMBEDDING MODEL
######################################################

model = SentenceTransformer("all-MiniLM-L6-v2", truncate_dim=N_DIMENSIONS)

def embedding_of_text(text: str):
    return model.encode(text).tolist()

######################################################
# PARSE GPT HISTORY AND PRODUCE EMBEDDINGS
######################################################

texts = []
embeddings = []

for conversation in data[:1250]:
    print(conversation["title"])
    for message in conversation["mapping"].values():
        if (
            message["message"] is None
            or message["message"]["content"]["content_type"] != "text"
        ):
            continue
        if not message["message"]["content"]["parts"]:
            continue

        for part in message["message"]["content"]["parts"]:
            if not part:
                continue
            texts.append(part)


print(len(texts))
for text in texts:
    embeddings.append(embedding_of_text(text))

######################################################
# DIMENSIONALITY REDUCTION
######################################################

reducer = UMAP(metric="cosine")
embeddings_2d = reducer.fit_transform(embeddings)

######################################################
# PRODUCE WIZMAP OUTPUT
######################################################

xs = embeddings_2d[:, 0].astype(float).tolist()
ys = embeddings_2d[:, 1].astype(float).tolist()
data_list = wizmap.generate_data_list(xs, ys, texts)
grid_dict = wizmap.generate_grid_dict(xs, ys, texts, "Chat History")

######################################################
# EXPORT DATA
######################################################

wizmap.save_json_files(data_list, grid_dict, output_dir="./")
