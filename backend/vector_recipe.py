from openai import OpenAI
from pinecone import Pinecone 
from typing import List
from config import OPENAI_API_KEY, PINECONE_API_KEY
from utils import eng_to_jp

class SimilarTitle:
    """
    Singleton class to recommend recipes based on similarity to a given title using Pinecone.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SimilarTitle, cls).__new__(cls)
            cls._instance._initialize(*args, **kwargs)
        return cls._instance

    def _initialize(self):
        """
        Initialize Pinecone client and OpenAI embedding model.
        """
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.pinecone = Pinecone(api_key=PINECONE_API_KEY)
        self.index = self.pinecone.Index("cookpad-recipe") 

    def _get_user_vector(self, title: str) -> List[float]:
        response = self.client.embeddings.create(
            input=[title],
            model="text-embedding-3-small",
            dimensions = 512 
        )
        return response.data[0].embedding

    def _query_index(self, vector: List[float], k: int = 10) -> List[str]:
        result = self.index.query(
            vector=vector,
            top_k=k,
            include_metadata=True
        )
        return [
        {
            "id": match.id,
            "score": match.score,
            **match.metadata  # includes title, url, category, etc.
        }
        for match in result.matches
        ]   


    def get_top_k(self, user_title: str, k: int = 10) -> List[str]: 
        # user title (eng -> jp)
        query_jp = eng_to_jp(user_title)
        user_vector = self._get_user_vector(query_jp)
        return self._query_index(user_vector, k)


# if __name__ == "__main__":

#     user_title = "ぶたしゃぶ"

#     similar_title = SimilarTitle()
#     recommendations = similar_title.get_top_k(user_title, k=5)

#     print("Recommended recipes:")
#     print(recommendations)