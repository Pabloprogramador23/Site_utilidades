from embedchain.embedder.base import BaseEmbedder
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()

class GeminiEmbedder(BaseEmbedder):
    def __init__(self, model="embedding-001"):
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel(model)

    def embed(self, text: str):
        res = self.model.embed_content(content=text, task_type="retrieval_document")
        return res["embedding"]

    def embed_documents(self, texts):
        return [self.embed(t) for t in texts]

    def embed_query(self, text):
        return self.embed(text)
