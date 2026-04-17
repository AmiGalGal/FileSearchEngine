from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch
from sentence_transformers import util
import torch.nn.functional as F

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")


def PathToImg(path):
    img = Image.open(path)
    return img

def ImgToVector(path):
    img = PathToImg(path)

    inputs = processor(images=img, return_tensors="pt")

    with torch.no_grad():
        image_features = model.get_image_features(**inputs)

    return image_features

def TextToVector(text):
    inputs = processor(
        text=text,
        return_tensors="pt",
        padding=True,
        truncation=True
    )

    with torch.no_grad():
        text_features = model.get_text_features(**inputs)

    return text_features

def similarity(query_emb, image_emb):
    return util.cos_sim(query_emb, image_emb)

x = TextToVector("toilet")
#print(type(x))

#y = ImgToVector(r"C:\Users\amiel\PycharmProjects\PythonProject\ImgSearchEngine\Files\Balls4.png")
#print(type(y))

#print(similarity(x, y))
