from openai import OpenAI

# pip install openai
# if you saved the key under a different environment variable name, you can do something like:
client = OpenAI(
    api_key="pub_efd2a7c74921469785539905553be0c4",
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
