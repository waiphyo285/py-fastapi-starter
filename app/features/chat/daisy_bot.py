import os
from base_bot import BaseChatBot

class PortfolioBot(BaseChatBot):
    def dataset_path(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_dir, "..", "datasets", "portfolio.csv")

    def fields(self):
        return ["title", "details", "repo_desc"]

    def sample_questions(self):
        return [
            "Tell me about your POS system experience.",
            "What skills do you use most in backend development?",
            "How do you ensure your applications are scalable?"
        ]

    def prompt_builder(self, question, data):
        return f"""
            You are a helpful assistant that improves and enhances short sentences or notes by rewriting them into a polished, natural, and fluent paragraph.

            Here are some notes from a software engineer's profile and projects:

            Title: {data['title']}
            Details: {data['details']}
            Repository Desc: {data['repo_desc']}

            Based on the above, answer the following question clearly and naturally:

            Question: {question}
        """

bot = PortfolioBot() 
bot.run()