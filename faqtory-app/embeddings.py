from langchain_openai import OpenAIEmbeddings
from config.settings import settings

class Embeddings:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small", dimensions=1024, api_key=settings.secrets["openai_api_key"])

    def initialize_embeddings(self):
        return self.embeddings

    def encode_chunks(self, text: str) -> list[float]:
        return self.embeddings.embed(text)