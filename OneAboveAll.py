import os
from VideoSearchEngine import VideoIndexer, VideoRetriever
from ImgSearchEngine import ImgIndexer, ImgRetriever
from DocSearchEngine import Indexer, Retriever
import json

def getFiles(folder):
    videos = VideoIndexer.getFiles(folder)
    imgs = ImgIndexer.getFiles(folder)
    docs = Indexer.getFiles(folder)
    return videos, imgs, docs

def CreateDBs(videos, imgs, docs, VideoName = "lcLihsJnwlIt.json", ImgName = "PPlqqUxaMfzL.json", DocName = "ktqdmCptcsXM.json"):
    VideoIndexer.Createjson(VideoIndexer.getVectors(videos),videos, VideoName)
    ImgIndexer.Createjson(ImgIndexer.getVectors(imgs),imgs, ImgName)
    texts, paths, chunks = Indexer.FilesToText(docs)
    vecs = Indexer.Text2Vec(texts)
    Indexer.Createjson(vecs, paths, chunks, DocName)

def Create(folder):
    videos, imgs, docs = getFiles(folder)
    CreateDBs(videos, imgs, docs)

def search(query, type, top = 1):
    if type == 0:
        DB = "ktqdmCptcsXM.json"
        files = Retriever.search(query, DB, top)
    elif type == 1:
        DB = "PPlqqUxaMfzL.json"
        files = ImgRetriever.search(query, DB, top)
    elif type == 2:
        DB = "lcLihsJnwlIt.json"
        files = VideoRetriever.search(query, DB, top)
    else:
        files = []
    return files

