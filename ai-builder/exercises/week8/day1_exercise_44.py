from dotenv import load_dotenv
import anthropic

def get_weather(city):
    return {"city": city, "temp": "15°C", "condition": "cloudy"}

def calculate(expression):
    return str(eval(expression))

def get_current_time(timezone):
    return "14:32 CET"



tools = [
    {
        "name": "get_weather",
        "description": "Get current weather for a city. Use this when the user asks about weather.",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The city name, e.g. 'London'"
                }
            },
            "required": ["city"]
        }
    },
    {
        "name": "get_current_time",
        "description": "Get current time for a timezone. Use when the user ask about the time in a timezone",
        "input_schema": {
            "type": "object",
            "properties": {
                "timezone": {
                    "type": "string",
                    "description": "A timezone, e.g. 'CET'"
                }
            },
            "required": ["timezone"]
        }
    },
    {
        "name": "calculate",
        "description": "Takes a numerical equation string and calculates the resulting value. Use when the user ask to perform mathematical operations",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Numerical operation, e.g. '5 + 3'"
                }
            },
            "required": ["expression"]
        }
    }

]

load_dotenv()
client = anthropic.Anthropic()

tool_functions = {
    "get_weather": get_weather,
    "calculate": calculate,
    "get_current_time": get_current_time
}

response_list = [
    {
        "role": "user",
        "content": "What's the weather in Paris and what's 123 times 456?"
        }
    ]

max_iterations = 10
iteration = 0

while iteration < max_iterations:
    iteration += 1
    print(f"\n ---Step {iteration} ---")

    response = client.messages.create(
        model = "claude-haiku-4-5-20251001",
        max_tokens = 2048,
        messages = response_list,
        tools = tools
    )

    response_list.append(
        {
            "role": "assistant",
            "content":response.content
            }
        )

    print(response.stop_reason)
    if response.stop_reason == "end_turn":
        print("\nFinal answer:")
        print(response.content[0].text)
        break

    tool_results = []

    for resp in response.content:
        print(resp.type)

        if resp.type == "tool_use":
            function_to_call = tool_functions[resp.name]
            result = function_to_call(**resp.input)
            print(f"Called {resp.name}, got: {result}")
            tool_results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": resp.id,
                    "content": str(result)
                    }
            )

    response_list.append(
        {
            "role": "user",
            "content": tool_results
            }
        )



