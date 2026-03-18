# Week 2 Exercise 8
import anthropic
from dotenv import load_dotenv
import os

def ask_claude(question, system_prompt=None):
    
    # Step 1: Load environment variables
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")

    # Step 2: Check that we have a key before proceeding
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not found in .env file")
        print("Add it like: ANTHORPIC_API_KEY=sk-ant-your-key-here")
        return None
    else:
        # Step 3: Create the client
        client = anthropic.Anthropic(api_key=api_key)

        # Step 4: Send a message
        try:
            kwargs = {
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 1024,
                "messages": [
                    {"role": "user", "content": question}
                ]
            }

            if system_prompt:
                kwargs["system"] = system_prompt

            response = client.messages.create(**kwargs)

            # Step 5: Print response
            print("Claude says:")
            print(response.content[0].text)

            # Step 6: Print usage info
            print(f"\nTokens used - input: {response.usage.input_tokens}, output: {response.usage.output_tokens}")

            return response.content[0].text
        except anthropic.AuthenticationError:
            print("Error: Invalid API key. Check your ANTHROPIC_API_KEY.")
            return None
        except anthropic.APIConnectionError:
            print("Error: Can't connect to the API. Check your internet.")
            return None
        except anthropic.APIError as e:
            print(f"API error: {e}")
            return None

answer = ask_claude("What is Python?")
answer = ask_claude("What is Python?", system_prompt="Respond as a pirate")