#File purpose: get a query and return the app file

import json
import numpy as np
from . import Embedder
from . import Parser

def load_json(file_path):
    vectors = []
    filenames = []
    chunks = []

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        vectors.append(np.array(item["vector"]))
        filenames.append(item["filename"])
        chunks.append(item["chunk"])

    return vectors, filenames, chunks

def FindBest(vectors, filenames, chunks, query):
    length = len(filenames)
    queryVec = Embedder.embed(query)
    scores = []
    indexes = []
    for i in range(0, length):
        score = Embedder.similarity(queryVec, vectors[i])
        scores.append(score)
        indexes.append(i)
    sortedIdx = sorted(zip(scores, indexes), reverse=True)
    scores, indexes = zip(*sortedIdx)
    return indexes

def extractText(vectors, filenames, chunks, index):
    FullText = Parser.DocToText(filenames[index])
    words = FullText.split()
    chunk_words = words[chunks[index]:chunks[index]+250]
    chunk_text = " ".join(chunk_words)
    return chunk_text

def search(query, DB= "ktqdmCptcsXM.json", top = 3):
    v,f,c = load_json(DB)
    q = query
    bi = FindBest(v,f,c,q)
    files = []
    texts = []
    top = min(top, len(bi))
    for i in range(top):
        files.append(f[bi[i]])
        texts.append(extractText(v,f,c,bi[i]))

    return files, texts