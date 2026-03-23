import anthropic
import os
from dotenv import load_dotenv
import json

def extract_json(text):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    start = text.find("[")
    end = text.rfind("]") + 1

    if start != -1 and end > start:
        try:
            return json.loads(text[start:end])
        except json.JSONDecodeError:
            pass
    
    start = text.find("{")
    end = text.rfind("}") + 1
    if start != -1 and end > start:
        try:
            return json.loads(text[start:end])
        except json.JSONDecodeError:
            pass
    
    return None

# Excercise 32a:
def chain_summarize_then_extract(text):
    
    try:
        response_1 = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[{"role": "user", "content": f"Summarize this text in 2-3 sentences:\n\n{text}"}]
        )
    except anthropic.AuthenticationError:
        print("Invalid API key")
        return None
    except anthropic.APIConnectionError:
        print("Network error")
        return None
    except anthropic.APIError as e:
        print(f"API error: {e}")
        return None

    summary = response_1.content[0].text

    try:
        response_2 = client.messages.create(
            model = "claude-sonnet-4-20250514",
            max_tokens = 1024,
            messages=[{"role": "user", "content": f"Extract action items from this summary\n\n{summary}"}],
            system= """You are a data extraction assistant. Respond ONLY with a valid JSON array. No extra text, no markdown.
            Use exactly this structure in your response:
            [
            {"owner": "name", "task": "what they need to do", "deadline": "date or null if unknown"}
            ]"""
        )
    except anthropic.AuthenticationError:
        print("Invalid API key")
        return None
    except anthropic.APIConnectionError:
        print("Network error")
        return None
    except anthropic.APIError as e:
        print(f"API error: {e}")
        return None
    
    raw_text = response_2.content[0].text
    action_items = extract_json(raw_text)

    total_input = response_1.usage.input_tokens + response_2.usage.input_tokens
    total_output = response_1.usage.output_tokens + response_2.usage.output_tokens

    result_dic = {
        "summary": summary,
        "action_items": action_items,
        "input_tokens": total_input,
        "output_tokens": total_output

    }

    return result_dic


load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=api_key)

sample_text = """
Meeting with the product team ran long. We decided to push the launch 
to Q2. Sarah will update the roadmap by Thursday. Budget approval is 
still pending from finance — Marco needs to follow up with them. 
The new pricing model was well received. Next sync is scheduled for 
Monday at 10am. John needs to send the updated deck to stakeholders 
before then.
"""
result = chain_summarize_then_extract(sample_text)

if result is None:
    print("Something went wrong")
else:
    print(f"Summary:\n{result['summary']}\n\n")
    for action_item in result['action_items']:
        if action_item.get("deadline") is None:
            print(f"   - {action_item['owner']}: {action_item["task"]} (no deadline)\n")
        else:
            print(f"   - {action_item['owner']}: {action_item['task']} (due: {action_item['deadline']})\n")
    print(f"Total input tokens: {result['input_tokens']}\n")
    print(f"Total output tokens: {result['output_tokens']}\n")
