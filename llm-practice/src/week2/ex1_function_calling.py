"""Week 2 exercise 1 — the function-calling loop, hands-on.

Based on the OpenAI Cookbook:
https://cookbook.openai.com/examples/how_to_call_functions_with_chat_models

Fill in the 6 sections marked TODO. Run with:

    uv run python src/week2/ex1_function_calling.py

Expected output (model choice may vary the prose, but the structure is fixed):

    Step 1: model asked to call get_current_weather(location='San Francisco, CA', unit='celsius')
    Step 2: function result: {'location': 'San Francisco, CA', 'temperature': 14, 'unit': 'celsius', 'forecast': 'foggy'}
    Step 3: final answer: <some natural-language answer mentioning 14 celsius>

If you get stuck, the answer pattern is in the cookbook link above. Don't
copy-paste — write it yourself, even if you consult the cookbook.
"""
from __future__ import annotations

import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://ollama.com/v1",
    api_key=os.environ["OLLAMA_API_KEY"],
)

MODEL = "kimi-k3:cloud"  # or whichever model worked for you


# ---------------------------------------------------------------------------
# The function the model is allowed to "call".
# The model never runs this — it just emits JSON args; YOU run it.
# ---------------------------------------------------------------------------
def get_current_weather(location: str, unit: str = "fahrenheit") -> dict:
    """Fake weather service. Real code would call OpenWeatherMap here."""
    return {
        "location": location,
        "temperature": 14 if unit == "celsius" else 57,
        "unit": unit,
        "forecast": "foggy",
    }


# ---------------------------------------------------------------------------
# TODO 1: define the tool schema.
#
# A list with one entry of type "function". The function has a name,
# description, and a JSON-Schema `parameters` object with `location`
# (required string) and `unit` (optional string enum of celsius/fahrenheit).
# ---------------------------------------------------------------------------
tools: list[dict[str, dict[str, str]]] = [{
    "type": "function",
    "function": {
        "name": "get_current_weather",
        "description": "Get the current weather for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA"
                },
                "unit": {
                    "type": "string",
                    "description": "The unit of temperature (celsius or fahrenheit)",
                    "enum": ["celsius", "fahrenheit"]
                }
            },
            "required": ["location"]
        }
    }
}]


# ---------------------------------------------------------------------------
# TODO 2: first request — user asks about the weather, tools attached.
# ---------------------------------------------------------------------------
USER_QUESTION = "What's the weather like in San Francisco? Use celsius."


def main() -> None:
    messages = [{"role": "user", "content": USER_QUESTION}]

    # TODO 2: first response = client.chat.completions.create(
    #     model=MODEL, messages=messages, tools=tools, tool_choice="auto"
    # )
    first_response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    assistant_message = first_response.choices[0].message

    # TODO 3: if assistant_message.tool_calls exists, pull the first entry.
    # It has .id, .function.name, and .function.arguments (a JSON string).
    # Parse the arguments string into a dict with json.loads().
    # Print: Step 1: model asked to call <name>(<kwargs inline>)
    tool_call = assistant_message.tool_calls[0] if assistant_message.tool_calls else None
    function_name = tool_call.function.name if tool_call else None
    function_args = json.loads(tool_call.function.arguments) if tool_call else None
    args_repr = ", ".join(f"{k}={v!r}" for k, v in (function_args or {}).items())
    print(f"Step 1: model asked to call {function_name}({args_repr})")

    # TODO 4: call the actual Python function with **function_args.
    function_result = get_current_weather(**function_args) if function_args else None
    print(f"Step 2: function result: {function_result}")

    # TODO 5: append BOTH messages onto `messages`:
    #   a) the assistant_message itself (it carries the tool_call)
    #   b) {"role": "tool", "tool_call_id": tool_call.id,
    #       "content": json.dumps(function_result)}
    # This is how the model gets the function's output back.
    messages.extend([
        assistant_message,
        {
            "role": "tool",
            "tool_call_id": tool_call.id if tool_call else None,
            "content": json.dumps(function_result) if function_result else None
        }
    ])

    # TODO 6: second call with the extended messages list — no tools arg
    # this time. The model writes the final natural-language answer.
    final_response = client.chat.completions.create(
        model=MODEL,
        messages=messages
    )
    print(f"Step 3: final answer: {final_response.choices[0].message.content}")


if __name__ == "__main__":
    main()
