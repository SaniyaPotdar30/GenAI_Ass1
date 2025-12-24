import chromadb

db = chromadb.PersistentClient(path="./knowledge_base")
collection = db.get_or_create_collection("resumes")

print(collection)
