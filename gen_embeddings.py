from flask import Flask, request, jsonify
import pandas as pd
import cohere as ch
import chromadb
from unstructured.partition.html import partition_html
from unstructured.chunking.title import chunk_by_title
import time
import itertools
import os
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

def get_chunks():
    for root, dirs, files in os.walk("/Users/sunchipnacho/Temp/umass"):
        for file in files:
            try:
                with open(os.path.join(root, file), "r") as f:
                    text = f.read()

                    elements = partition_html(text=text)
                    for chunk in chunk_by_title(elements):
                        yield str(chunk).strip().replace("\n", " ")
            except Exception as e:
                continue


def get_collection():
    client = chromadb.PersistentClient(path="db")
    ef = chromadb.utils.embedding_functions.CohereEmbeddingFunction(
        api_key=key, model_name="embed-english-v3.0"
    )
    collection = client.get_or_create_collection("main", embedding_function=ef)
    return collection


def embed_chunks(docs, collection, offset=0):
    try:
        collection.add(
            documents=docs,
            metadatas=[{"source": f"doc-{i + offset}"} for i in range(len(docs))],
            ids=[f"doc-{i + offset}" for i in range(len(docs))],
        )
    except Exception as e:
        print(f"Error: {e}")
        with open("error.txt", "w") as f:
            f.write(str(e))
        return


chunks = get_chunks()
offset = 0
collection = get_collection()

for chunks in itertools.batched(chunks, 90):
    embed_chunks(list(chunks), collection, offset)
    offset += 90
