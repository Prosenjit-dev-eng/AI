from openai import OpenAI
from dotenv import load_dotenv
from tools import TOOLS,run_tool
from Utilities.utilities import log
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
# Chat loop starts here

while True:
    user_input = input("Prosenjit: ")
    if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
        print("Exiting the chat. Goodbye!")
        break

    messages.append({"role": "user", "content": user_input})    

    MAX_STEPS = 5  # Limit the number of tool calls to prevent infinite loops

    for step in range(MAX_STEPS):
        response = client.chat.completions.create(
            model=os.getenv("MODEL"),  # Set the model name for the chat completion
            messages=messages,
            tools=TOOLS,
        )
        msg = response.choices[0].message

        if not msg.tool_calls:
            break  # No tool calls, exit the inner loop

        log(f"Step {step + 1}: model requested {len(msg.tool_calls)} tool call(s).")
        
        messages.append(msg)  # Add the tool call message to the chat history

        for tool_call in msg.tool_calls:
            result = run_tool(tool_call)  # Execute the tool call and get the result
            messages.append({
                "role": "tool",
                "tool_call_id":tool_call.id,
                "content": str(result)
                })  # Add the tool's response to the chat history


    # How do I know I get break or not?
    else:
        # If the loop completes without a break, it means the maximum number of steps was reached, we ran out of steps
        # And the assistant did not finish the conversation, so we can print a message indicating that the maximum number of steps was reached.
        fallback = "Maximum number of steps reached. Please try again with a different query."
        messages.append({
            "role": "Assistant",
            "content": fallback
        })
        print("Assistant: ", fallback)
        continue
    # Chat history is added
    messages.append({"role": "assistant", "content": msg.content})    

    # in python we can access the content of the message using msg.content
    print("Assistant: " + (msg.content or ""))


# Ollama->JSON(response) to OpenAI->Python object(chat completion) conversion is done automatically by the OpenAI Python SDK.