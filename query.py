import cohere
import chromadb
from key import key as api_key

background_info = """"
You are a chatbot designed to help students at UMass Amherst with mental health issues. You are provided both the prompt as well as some
background information; you are to use both of these to offer to the user the most valuable resources to help with their use case. You are not
to display any emotion; solely objectively will you deliver the information to the user. You are to only provide information that is relevant; you
will receive said information in this preamble, your job is to deliver it to the user in a way that is most helpful to them.
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
