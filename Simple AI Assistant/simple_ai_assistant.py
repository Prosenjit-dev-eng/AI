from openai import OpenAI
from dotenv import load_dotenv
from tools import TOOLS, FUNCTION_NAME_TO_FUNCTION_MAP
import json
import os

load_dotenv()  # Load environment variables from .env file
client = OpenAI(
    base_url = os.getenv("BASE_URL"),  # Set the base URL for the OpenAI API
    api_key = os.getenv("API_KEY")# No need for ollama model, just use the OpenAI API key
)
messages = []
# Smarter way to set the system message for the assistant's behavior
messages.append({"role": "system", "content": "Act like a very humble agent and respond always under 20 words"})  # System message to set the behavior of the assistant
while True:
    user_input = input("Prosenjit: ")
    if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
        print("Exiting the chat. Goodbye!")
        break

    messages.append({"role": "user", "content": user_input})    

    response = client.chat.completions.create(
        model=os.getenv("MODEL"),  # Set the model name for the chat completion
        messages=messages,
        tools=TOOLS,
    )

    msg = response.choices[0].message
    if msg.tool_calls:
        messages.append(msg)  # Add the tool call message to the chat history
        for tool_call in msg.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments) #function_args is a dictionary of the function arguments

            fn = FUNCTION_NAME_TO_FUNCTION_MAP[function_name]
            result = fn(**function_args)

            messages.append({"role": "tool",
                             "tool_call_id":tool_call.id,
                              "content": str(result)})  # Add the tool's response to the chat history
        #2nd call to the LLM to get the final response after tool execution
        response = client.chat.completions.create(
            model=os.getenv("MODEL"),
            messages=messages
        )
        msg = response.choices[0].message
    # Chat history is added
    messages.append({"role": "assistant", "content": response.choices[0].message.content})    

    print("Assistant: ")
    print(response.choices[0].message.content)


# Ollama->JSON(response) to OpenAI->Python object(chat completion) conversion is done automatically by the OpenAI Python SDK.