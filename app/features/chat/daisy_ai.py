import os
import random
import openai
import pandas as pd
from sentence_transformers import SentenceTransformer, util

openai.api_key = 'sk-proj-xxx'

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
    return ""

# Create a prompt for OpenAI
def create_prompt(question, title, details, repo_desc):
    prompt = f"""
        You are a helpful assistant that improves and enhances short sentences or notes by rewriting them into a polished, natural, and fluent paragraph.

        Here are some notes from a software engineer's profile and projects:

        Title: {title}
        Details: {details}
        Repository Desc: {repo_desc}

        Based on the above, answer the following question clearly and naturally:

        Question: {question}
    """
    return prompt

# Function to ask OpenAI
def ask_openai(prompt):
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

# Test it
questions = [
    "Tell me about your POS system experience.",
    "What skills do you use most in backend development?",
    "What experience do you have with cloud platforms like AWS?",
    "Can you describe a time when you optimized performance in a project?",
    "How do you handle database design and management?",
    "What testing frameworks do you prefer for backend and frontend?",
    "How do you approach debugging complex issues?",
    "Describe your experience working in Agile or Scrum teams.",
    "What are some best practices you follow for REST API development?",
    "How do you keep your codebase secure from common vulnerabilities?",
    "Have you worked with microservices architecture? If so, how?",
    "What tools do you use for continuous integration and deployment?",
    "How do you ensure your applications are scalable?",
    "Can you explain your approach to documentation and knowledge sharing?",
    "What are your core values as a software engineer?",
    "Have you contributed to any open-source projects? Tell me about them.",
    "How do you balance between meeting deadlines and writing clean code?",
    "What strategies do you use to mentor junior developers?",
    "Describe a feature you designed from scratch and its impact.",
    "How do you stay updated with the latest technology trends?",
    "Can you tell me about yourself and your journey as a software engineer?"
]


idx = random.randint(0, 19)
ask = questions[idx]
ans = get_answer(ask)
title = safe_get(ans["title"])
details = safe_get(ans["details"])
repo_desc = safe_get(ans["repo_desc"])

prompt = create_prompt(ask, title, details, repo_desc)
enhanced_answer = ask_openai(prompt)

print(f"Q: {ask}")
print(f"A: {enhanced_answer}")

# Run the script
# python3 app/features/chat/daisy_ai.py
