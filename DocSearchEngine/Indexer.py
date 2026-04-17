#File purpose: finding the files and storing the chunks in the files

import os
from . import Parser
from . import Embedder
import json

def getFiles(folder):
    allowed = [".pdf", ".docx", ".txt", ".md"]
    final_list = []

    for root, dirs, files in os.walk(folder):
        for f in files:
            suffix = os.path.splitext(f)[1].lower()

            if suffix in allowed:
                full_path = os.path.join(root, f)
                final_list.append(full_path)

    return final_list

def FilesToText(Files):
    texts = []
    files_path = []
    chunks = []
    for f in Files:
        text = Parser.DocToText(f)
        words = text.split()
        for i in range(0, len(words), 250):
            chunks.append(i)
            files_path.append(f)
            chunk_words = words[i:i + 250]
            chunk_text = " ".join(chunk_words)
            texts.append(chunk_text)
    return texts, files_path, chunks

def Text2Vec(sentences):
    vecs = []
    for text in sentences:
        vecs.append(Embedder.embed(text))
    return vecs

def Createjson (vecs, files, chunks, output):
    data = []
    for vector, filename, chunk in zip(vecs, files, chunks):
        data.append({
            "vector": vector.tolist(),
            "filename": filename,
            "chunk": chunk
        })

    with open(output, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def createDB(Folder, name = "ktqdmCptcsXM.json"):
    Files = getFiles(Folder)
    texts, paths, chunks = FilesToText(Files)
    vecs = Text2Vec(texts)
    Createjson(vecs, paths, chunks, name)

