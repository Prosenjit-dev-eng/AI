from datetime import datetime
import requests
def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S");

def get_city_weather(city):
    # Placeholder implementation for getting city weather
    url = f"https://wttr.in/{city}?format=3"
    # In a real implementation, you would call a weather API here
    response = requests.get(url,timeout = 10)
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
}