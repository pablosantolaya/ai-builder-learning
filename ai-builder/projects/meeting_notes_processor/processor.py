from dotenv import load_dotenv
import json
import anthropic
import os
from config import MODEL, MAX_TOKENS, SYSTEM_PROMPT

def extract_json(text):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    start = text.find("{")
    end = text.rfind("}") + 1
    if start != -1  and end > start:
        try:
            return json.loads(text[start:end])
        except json.JSONDecodeError:
            pass

    return None

def process_transcript(content):
    
    # Create client
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not found in environment variables.")
        return None
    
    try:
        client = anthropic.Anthropic(api_key = api_key)
        response = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            messages=[{"role":"user", "content": content}],
            system=SYSTEM_PROMPT
        )
    
        parsed = extract_json(response.content[0].text)

        if parsed is None:
            print("Failed to parse JSON from response")
            return None

        results = {
            "parsed_data": parsed,
            "model": response.model,
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens
        }
        
        return results


    except anthropic.AuthenticationError:
        print("Invalid API key")
    except anthropic.APIConnectionError:
        print("Network error")
    except anthropic.APIError as e:
        print(f"API error: {e}")