from openai import OpenAI

# pip install openai
# if you saved the key under a different environment variable name, you can do something like:
client = OpenAI(
    api_key="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",
)

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": "You are a virtual assistant named bestie skilled in general tasks like Alexa and Google Cloud",
        },
        {"role": "user", "content": "what is coding"},
    ],
)

print(completion.choices[0].message.content)
