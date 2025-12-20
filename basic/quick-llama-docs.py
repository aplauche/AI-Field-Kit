from llama_index.core import SimpleDirectoryReader, VectorStoreIndex

# By default looks for OPENAI_API_KEY in environment vars

docs = SimpleDirectoryReader('docs').load_data()

index = VectorStoreIndex.from_documents(docs)

query_engine = index.as_query_engine()

response = query_engine.query("what do the docs say about ______?")

print(response)

# To persist data (under ./storage)

index.storage_context.persist()

# To reload from disk:

from llama_index.core import StorageContext, load_index_from_storage

# rebuild storage context
storage_context = StorageContext.from_defaults(persist_dir="./storage")

# load index
index = load_index_from_storage(storage_context)

