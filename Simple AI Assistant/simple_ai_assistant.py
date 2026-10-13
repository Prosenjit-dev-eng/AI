from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file
client = OpenAI(
    base_url = os.getenv("BASE_URL"),  # Set the base URL for the OpenAI API
    api_key = os.getenv("API_KEY")# No need for ollama model, just use the OpenAI API key
)
messages = []
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
        print("Exiting the chat. Goodbye!")
        break

    messages.append({"role": "user", "content": user_input})    

    response = client.chat.completions.create(
        model=os.getenv("MODEL"),  # Set the model name for the chat completion
        messages=messages
    )
    # Chat history is added
    messages.append({"role": "assistant", "content": response.choices[0].message.content})    

    print("LLM response: ")
    print(response.choices[0].message.content)


# Ollama->JSON(response) to OpenAI->Python object(chat completion) conversion is done automatically by the OpenAI Python SDK.