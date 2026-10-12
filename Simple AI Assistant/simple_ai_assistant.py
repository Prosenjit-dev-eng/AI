from openai import OpenAI

client = OpenAI(
    base_url = "http://localhost:11434/v1",
    api_key = "dummy_api_key"# No need for ollama model, just use the OpenAI API key
)

response = client.chat.completions.create(
  model="qwen3:4b",
  messages=[
    {"role": "user", "content": "Hello!"}
  ]
)
print("LLM response: ")
print(response.choices[0].message.content)

# Ollama->JSON(response) to OpenAI->Python object(chat completion) conversion is done automatically by the OpenAI Python SDK.