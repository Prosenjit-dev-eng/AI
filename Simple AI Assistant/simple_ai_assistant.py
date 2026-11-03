from types import SimpleNamespace

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
messages.append({"role": "system", "content": 
                    "You are a helpful, humble assistant. "
                    "Answer general questions (programming, science, advice) from your own knowledge. "
                    "Use a tool ONLY when the user asks for the current time, the weather, or their city. "
                    "Keep answers under 100 words."
                })  # System message to set the behavior of the assistant
# Chat loop starts here

def stream_chat(history):
    stream = client.chat.completions.create(
        model=os.getenv("MODEL"),  # Set the model name for the chat completion
        messages=history,
        tools=TOOLS,
        stream=True,
    )

    full_response = ""
    calls = {}   # index -> tool call being built
    label_printed = False
    #Streaming started
    try:
        for chunk in stream:
            if not chunk.choices:                       # some servers send chunks with no choices
                continue
            delta = chunk.choices[0].delta
            #1. Content streaming: Do we have message content in this chunk? If yes, print it to the console and append it to the full response.
            piece = delta.content
            if piece:
                if not label_printed:
                    print("Assistant: ", end="", flush=True)
                    label_printed = True
                print(piece, end="", flush=True) #streaming
                full_response += piece

            #2. Tool call streaming: Do we have tool calls in this chunk? If yes, build the tool call objects and store them in the calls dictionary.  
            for tc in (delta.tool_calls or []):
                obj = calls.setdefault(
                    tc.index,
                    SimpleNamespace(id=None, function=SimpleNamespace(name="", arguments="")),
                )
                if tc.id:
                    obj.id = tc.id
                if tc.function and tc.function.name:
                    obj.function.name += tc.function.name
                if tc.function and tc.function.arguments:
                    obj.function.arguments += tc.function.arguments
    except KeyboardInterrupt:
        print("\n{Streaming interrupted by user.}")
        calls = {}

    if not label_printed:
        print() #Move to the next line if no content was printed

    calls_list = []
    for key in sorted(calls):
        calls_list.append(calls[key])
    print()  # Move to the next line after streaming
    return full_response, calls_list
def build_tool_calls(tool_calls):
    # Convert tool calls to a list of dictionaries
    payload = []
    for tool_call in tool_calls:
        tool_call_dict = {
            "id": tool_call.id,
            "type": "function",
            "function": {
                "name": tool_call.function.name,
                "arguments": tool_call.function.arguments
            }
        }
        payload.append(tool_call_dict)
    return payload


while True:
    user_input = input("Prosenjit: ")
    if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
        print("Exiting the chat. Goodbye!")
        break

    messages.append({"role": "user", "content": user_input})    

    MAX_STEPS = 5  # Limit the number of tool calls to prevent infinite loops

    for step in range(MAX_STEPS):
        # response = client.chat.completions.create(
        #     model=os.getenv("MODEL"),  # Set the model name for the chat completion
        #     messages=messages,
        #     tools=TOOLS,
        # )
        full_response, tool_calls = stream_chat(messages)
        # msg = response.choices[0].message

        if not tool_calls:
            break  # No tool calls, exit the inner loop

        log(f"Step {step + 1}: model requested {len(tool_calls)} tool call(s).")
        
        messages.append({
            "role": "assistant",
            "content": full_response,
            "tool_calls": 
                build_tool_calls(tool_calls)
            
        })  # Add the tool call message to the chat history

        for tool_call in tool_calls:
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
            "role": "assistant",
            "content": fallback
        })
        print("Assistant: ", fallback)
        continue
    # Chat history is added

    # in python we can access the content of the message using msg.content


# Ollama->JSON(response) to OpenAI->Python object(chat completion) conversion is done automatically by the OpenAI Python SDK.