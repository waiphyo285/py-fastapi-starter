import os
import random
import pandas as pd
from sentence_transformers import SentenceTransformer, util

# Get the directory of the current script
base_dir = os.path.dirname(os.path.abspath(__file__))

# Build absolute path to the CSV file
csv_path = os.path.join(base_dir, "dataset.csv")

# Load CSV dataset
df = pd.read_csv(csv_path)

# Prepare searchable text
df["search_text"] = df.apply(lambda row: " ".join(
    str(val) for val in [
        row["category"], row["sub_category"], row["title"], row["company"],
        row["details"], row["repo_name"], row["repo_desc"], row["language"]
    ] if pd.notna(val)
), axis=1)

# Load model
# model = SentenceTransformer("all-MiniLM-L6-v2")
model = SentenceTransformer("paraphrase-MiniLM-L3-v2")

# Encode data
corpus_embeddings = model.encode(df["search_text"].tolist(), convert_to_tensor=True)

# Query function
def get_answer(query):
    query_embedding = model.encode(query, convert_to_tensor=True)
    hits = util.semantic_search(query_embedding, corpus_embeddings, top_k=1)[0]
    return df.iloc[hits[0]["corpus_id"]]

# Safely get details
def safe_get(*fields):
    for f in fields:
        if pd.notna(f):
            return f
    return "No details available."

# Test it
questions = [
    "Tell me about your POS system experience.",
    "What was your role at RingZero IT Services?",
    "Can you explain your contribution to Plus Talent?",
    "How did you build the SarNarPar LMS app?",
    "What skills do you use most in backend development?",
    "What technologies are you most comfortable with?",
    "Describe your experience with Docker and CI/CD.",
    "How do you use TypeScript in your projects?",
    "Tell me about a project where you integrated GraphQL.",
    "What is the burmese-measure GitHub repo about?",
    "What are your core values as a software engineer?",
    "What frontend frameworks do you work with?",
    "What projects have you done using React and Next.js?",
    "Explain your role in the TM2 Life Assurance project.",
    "How did you contribute to CloudE8’s ERP system?",
    "What is your biggest strength as a developer?",
    "How do you approach learning new technologies?",
    "Can you tell me about the Hyper POS project?",
    "What is your educational background?",
    "What inspired you to become a software engineer?"
]

idx = random.randint(0, 19)
ask = questions[idx]
ans = get_answer(ask)

print(f"Q: {ask}")
print(f"A: {safe_get(ans['title'])}, {safe_get(ans['details'])}, {safe_get(ans['repo_desc'])}")
