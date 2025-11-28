# agents.py
import os
from openai import OpenAI

client = OpenAI(
    api_key="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"
)


class AIAgentSystem:
    def __init__(self):
        self.memory = []

    def add_memory(self, user_input, response):
        self.memory.append({"user": user_input, "ai": response})
        if len(self.memory) > 10:
            self.memory.pop(0)

    def get_context(self):
        if not self.memory:
            return ""
        parts = [f"User: {m['user']}\nAssistant: {m['ai']}" for m in self.memory[-3:]]
        return "\n\n".join(parts)

    def process_query(self, query: str) -> str:
        context = self.get_context()
        prompt = f"{context}\n\nUser: {query}\nAssistant:"
        try:
            completion = client.chat.completions.create(
                model="gpt-4o-mini",  # or gpt-3.5-turbo if you prefer
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant named Bestie. Be concise.",
                    },
                    {"role": "user", "content": prompt},
                ],
            )
            answer = completion.choices[0].message.content
            self.add_memory(query, answer)
            return answer
        except Exception as e:
            return f"Error: {e}"
