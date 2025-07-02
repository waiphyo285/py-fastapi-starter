import os
from base_bot import BaseChatBot

class EmotionBot(BaseChatBot):
    def dataset_path(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_dir, "..", "datasets", "emotion.csv")

    def fields(self):
        return ["title", "post", "feelings"]

    def sample_questions(self):
        return [
            "Why do I always feel like I’m not enough?",
            "How do I handle the constant pressure to appear okay?",
            "What can help when I can’t stop thinking negative thoughts?"
        ]

    def prompt_builder(self, question, data):
        return f"""
            You are a caring and professional therapist. Your goal is to provide a thoughtful, empathetic, and supportive response based on the emotional context.

            Here is the situation:

            Title: {data['title']}
            Post: {data['post']}
            Feelings expressed: {data['feelings']}

            Now, please answer the following question or respond gently and constructively, considering the feelings and the content of the post:

            Question: {question}
        """
        
bot = EmotionBot() 
bot.run()