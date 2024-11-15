import cohere
import chromadb
from key import key

background_info = """"
## Task & Context
You are an AI agent whose sole purpose is to provide mental health resources at the University of Massachusetts Amherst (also known as UMass Amherst or UMass)
If there is any other topic of conversation outside of mental health resources explain that you are trained to only discuss mental health resources. Keep in mind that the two major resources are University Health Services (UHS) and Center for Counseling and Psychological Health (CCPH)
## Style Guide

When listing resources, use a numbered list and ensure the output is succinct, clear and readable. After each resource, add a new line character. Ensure only mental health resources are discussed

All content you return MUST be markdown formatted. This includes any text, links, lists, or other content you return. Whatever content you see that is important
must be bolded according to markdown formatting. Lists should not be numbered but rather bulleted according to markdown standards.
"""

client = chromadb.PersistentClient(path="db")
ef = chromadb.utils.embedding_functions.CohereEmbeddingFunction(
    api_key=key, model_name="embed-english-v3.0"
)

collection = client.get_or_create_collection("main", embedding_function=ef)
co = cohere.ClientV2(api_key=key)


def get_relevant_docs(query: str):
    try:
        chunks = collection.query(
            query_texts=[query],
            n_results=30,
        )
        print(chunks)
    except Exception as e:
        print(f"Error: {e}")
        return []

    return chunks["documents"]


def answer_query(query: str):
    preamble = (
        background_info
        + "\n\n"
        + "## Background Info\n"
        + ". ".join(["".join(doc) for doc in get_relevant_docs(query)])
    )

    messages = [
        {
            "role": "system",
            "content": preamble,
        },
        {
            "role": "user",
            "content": query,
        },
    ]

    response_text = ""

    resp = co.chat_stream(
        model="command-r-plus",
        messages=messages,
        max_tokens=2000,
    )

    for event in resp:
        if event and event.type == "content-delta":
            response_text += event.delta.message.content.text

    return response_text


if __name__ == "__main__":
    while True:
        user_input = input("\nEnter your query: ")
        answer_query(user_input)
