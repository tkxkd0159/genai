import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("API_KEY"),
)
models = ["gpt-3.5-turbo"]

response = client.chat.completions.create(
    model=models[0],
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {
            "role": "assistant",
            "content": "The Los Angeles Dodgers won the World Series in 2020.",
        },
        {"role": "user", "content": "Where was it played?"},
    ],
    temperature=0,
)
print(response["choices"][0]["message"]["content"])


# Few-shot technique
# In some cases, it's easier to show the model what you want rather than tell the model what you want.
# To help clarify that the example messages are not part of a real conversation, and shouldn't be referred back to by the model,
# you can try setting the name field of system messages to example_user and example_assistant.
response = client.chat.completions.create(
    model=models[0],
    messages=[
        {
            "role": "system",
            "content": "You are a helpful, pattern-following assistant that translates corporate jargon into plain English.",
        },
        {
            "role": "system",
            "name": "example_user",
            "content": "New synergies will help drive top-line growth.",
        },
        {
            "role": "system",
            "name": "example_assistant",
            "content": "Things working well together will increase revenue.",
        },
        {
            "role": "system",
            "name": "example_user",
            "content": "Let's circle back when we have more bandwidth to touch base on opportunities for increased leverage.",
        },
        {
            "role": "system",
            "name": "example_assistant",
            "content": "Let's talk later when we're less busy about how to do better.",
        },
        {
            "role": "user",
            "content": "This late pivot means we don't have time to boil the ocean for the client deliverable.",
        },
    ],
    temperature=0,
)

print(response["choices"][0]["message"]["content"])

# An example of a faked few-shot conversation
# All example messages are part of a real conversation except the first one (system message).
response = client.chat.completions.create(
    model=models[0],
    messages=[
        {
            "role": "system",
            "content": "You are a helpful, pattern-following assistant.",
        },
        {
            "role": "user",
            "content": "Help me translate the following corporate jargon into plain English.",
        },
        {"role": "assistant", "content": "Sure, I'd be happy to!"},
        {"role": "user", "content": "New synergies will help drive top-line growth."},
        {
            "role": "assistant",
            "content": "Things working well together will increase revenue.",
        },
        {
            "role": "user",
            "content": "Let's circle back when we have more bandwidth to touch base on opportunities for increased leverage.",
        },
        {
            "role": "assistant",
            "content": "Let's talk later when we're less busy about how to do better.",
        },
        {
            "role": "user",
            "content": "This late pivot means we don't have time to boil the ocean for the client deliverable.",
        },
    ],
    temperature=0,
)

print(response["choices"][0]["message"]["content"])
