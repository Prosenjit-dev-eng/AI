from datetime import datetime
import json
from Utilities.utilities import log
import requests
def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S");
def get_user_city():
    return "Kolkata"
def get_city_weather(city):
    # Placeholder implementation for getting city weather
    url = f"https://wttr.in/{city}?format=3"
    # In a real implementation, you would call a weather API here
    response = requests.get(url,timeout = 10)
    response.raise_for_status() # Raise an exception for HTTP errors if something goes wrong with the request

    return response.text


#TOOLs = [{},{},..]
TOOLS = [
    {
        "type" : "function",
        "function" : {
            "name" : "current_time",
            "description" : "Returns the current date and time as a formatted string.",
            "parameters" : {
                "type" : "object",
                "properties" : {},  #here we put function arguments 
            }
        }
    },
    {
        "type" : "function",
        "function" : {
            "name" : "get_user_city",
            "description" : "Returns the user's city.",
            "parameters" : {
                "type" : "object",
                "properties" : {},  #here we put function arguments 
            }
        }
    },
    {
        "type" : "function",
        "function" : {
            "name" : "get_city_weather",
            "description" : "Returns the current weather for a given city.",
            "parameters" : {
                "type" : "object",
                "properties" : {
                    "city": {
                        "type": "string",
                        "description": "The name of the city to get the weather for."
                    }
                },
                "required": ["city"]
            }
        }
    }
]

FUNCTION_NAME_TO_FUNCTION_MAP = {
    "current_time" : current_time,
    "get_city_weather" : get_city_weather,
    "get_user_city" : get_user_city
}
def run_tool(tool_call):
            function_name = tool_call.function.name
            function_args = {}
            try:
                function_args = json.loads(tool_call.function.arguments) #function_args is a dictionary of the function arguments
                log(f"Tool call: {function_name} with arguments: {function_args}")
                fn = FUNCTION_NAME_TO_FUNCTION_MAP[function_name]
                result = fn(**function_args)

            except Exception as e:
                result = f"Error executing tool '{function_name}': {str(e)}"

            log(f"Tool result: {result}")
            return str(result)