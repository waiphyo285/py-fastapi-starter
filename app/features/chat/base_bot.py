import random
import openai
import pandas as pd
from abc import ABC, abstractmethod
from sentence_transformers import SentenceTransformer, util

openai.api_key = "sk-proj-xxx"

class BaseChatBot(ABC):
    def __init__(self):
        self.model = SentenceTransformer("paraphrase-MiniLM-L3-v2")
        self.df = None
        self.embeddings = None
        self.load_data()

    @abstractmethod
    def dataset_path(self) -> str:
        pass

    @abstractmethod
    def fields(self) -> list:
        pass

    @abstractmethod
    def prompt_builder(self, question: str, data: dict) -> str:
        pass

    @abstractmethod
    def sample_questions(self) -> list:
        pass

    def load_data(self):
        path = self.dataset_path()
        self.df = pd.read_csv(path)
        self.df["search_text"] = self.df.apply(self.row_to_text, axis=1)
        self.embeddings = self.model.encode(self.df["search_text"].tolist(), convert_to_tensor=True)

    def row_to_text(self, row) -> str:
        text_parts = []
        for field in self.fields():
            val = row.get(field, "")
            if field == "feelings" and isinstance(val, str):
                try:
                    val = " ".join(eval(val))
                except:
                    pass
            if pd.notna(val):
                text_parts.append(str(val))
        return " ".join(text_parts)

    def semantic_search(self, query: str) -> pd.Series:
        query_embedding = self.model.encode(query, convert_to_tensor=True)
        hits = util.semantic_search(query_embedding, self.embeddings, top_k=1)[0]
        return self.df.iloc[hits[0]["corpus_id"]]

    def safe_get(self, row, field):
        return row[field] if pd.notna(row[field]) else ""

    def ask_openai(self, prompt: str) -> str:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )
        return response.choices[0].message.content.strip()

    def run(self):
        question = random.choice(self.sample_questions())
        result_row = self.semantic_search(question)
        data = {field: self.safe_get(result_row, field) for field in self.fields()}
        prompt = self.prompt_builder(question, data)
        answer = self.ask_openai(prompt)

        print(f"Q: {question}\n")
        if "feelings" in data:
            print(f"A1: Expressed feelings: {data['feelings']}")
        print(f"A2: {answer}\n")
