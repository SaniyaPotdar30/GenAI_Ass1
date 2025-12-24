import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings

# Embedding model
embed_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Sample text
raw_text = """
Professional soccer players train daily.
They focus on endurance, skills, teamwork, and strategy.
Coaches help improve performance and fitness.
"""

# Split text into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=50,
    chunk_overlap=10
)
chunks = text_splitter.split_text(raw_text)

# ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="demo")

# Create embeddings
embeddings = embed_model.embed_documents(chunks)

ids = [f"doc_{i}" for i in range(len(chunks))]
metadatas = [{"source": "example.txt", "chunk_id": i} for i in range(len(chunks))]

# Add to DB
collection.add(
    ids=ids,
    documents=chunks,
    embeddings=embeddings,
    metadatas=metadatas
)

# Query
query = "How do soccer players train?"
query_embedding = embed_model.embed_query(query)

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=2
)

for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
    print(meta, "->", doc)

for distance in results["distances"][0]:
    print("Distance:", distance)

# Update
updated_text = "Professional soccer players train daily with coaches."
updated_embedding = embed_model.embed_documents([updated_text])

collection.add(
    ids=["doc_1"],
    documents=[updated_text],
    embeddings=updated_embedding,
    metadatas=[{"source": "example.txt", "chunk_id": 1}]
)

# Delete
collection.delete(where={"source": "example.txt"})
