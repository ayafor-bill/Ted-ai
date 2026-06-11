import chromadb

client = chromadb.PersistentClient(
    path="./database/chroma"
)

collection = client.get_or_create_collection(
    name="knowledge"
)


def add_note(text, note_id):
    collection.add(
        documents=[text],
        ids=[note_id]
    )


def search(query):

    results = collection.query(
        query_texts=[query],
        n_results=3
    )

    return results["documents"][0]
