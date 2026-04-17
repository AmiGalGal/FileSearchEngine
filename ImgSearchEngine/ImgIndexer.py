import os
from . import ImgEmbedder
import torch
import json
import numpy as np

def getFiles(folder):
    allowed = [".jpg", ".jpeg", ".jfif", ".png", ".webp", ".bmp"]
    final_list = []

    for root, dirs, files in os.walk(folder):
        for f in files:
            suffix = os.path.splitext(f)[1].lower()

            if suffix in allowed:
                full_path = os.path.join(root, f)
                final_list.append(full_path)

    return final_list

def getVectors(Files):
    vectors = []
    for f in Files:
        vectors.append(ImgEmbedder.ImgToVector(f))
    return vectors

def Createjson(vectors, files, output):

    data = []

    for vector, filename in zip(vectors, files):

        if hasattr(vector, "pooler_output"):
            vector = vector.pooler_output

        if torch.is_tensor(vector):
            vector = vector.detach().cpu().numpy()

        vector = np.array(vector).tolist()

        data.append({
            "vector": vector,
            "filename": filename
        })

    with open(output, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def createDB(Folder, name = "PPlqqUxaMfzL.json"):
    Files = getFiles(Folder)
    vectors = getVectors(Files)
    Createjson(vectors, Files, name)

