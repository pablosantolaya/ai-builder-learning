import json
import anthropic
from dotenv import load_dotenv
import os

def extract_json(text):
    """Try to extract and parse JSON from Claude's response text."""
    # First, try parsing the whole response directly
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # If that fails, look for JSON between curly braces
    start = text.find("{")
    end = text.rfind("}")+1
    if start != -1 and end > start:
        try:
            return json.loads(text[start:end])
        except json.JSONDecodeError:
            pass
    
    # Nothing worked
    return None


def extract_person_info(text):
    # Step 1: Load env and retrieve API key
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")

    # Step 2: Check that we have a key before proceeding
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not found in .env file")
        print("Add it like: ANTHROPIC_API_KEY=sk-ant-your-key-here")
        return None

    # Step 3: Create client
    client = anthropic.Anthropic(api_key=api_key)

    try:
        # Step 4: Send a message
        system_prompt = """You are a data extraction assistant.
        Respond ONLY with valid JSON. No extra text, no markdown, no explanation.
        If a field is missing use null as the value.
        use exactly this structure:
        {
            "name": "string or null",
            "job_title": "string or null",
            "company": "string or null",
            "location": "string or null",
            "interests": ["list", "of", "strings"] or [],
            "fields_missing": ["list of field names that couldn't be found"]
        }"""

        # Step 5 = Send message to LLM 
        response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": text}
                ]
            )    
        
        # Step 6 = Extract JSON
        response_json = extract_json(response.content[0].text)

        return response_json
        
    except anthropic.AuthenticationError:
        print("Error: Invalid API key. Check your ANTHROPIC_API_KEY.")
        return None
    except anthropic.APIConnectionError:
        print("Error: Can't connect to the API. Check your internet.")
        return None
    except anthropic.APIError as e:
        print(f"API error: {e}")
        return None



def analyze_text(text):
    
    # Step 1: Load env and retrieve API key
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")

    # Step 2: Check that we have a key before proceeding
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not found in .env file")
        print("Add it like: ANTHROPIC_API_KEY=sk-ant-your-key-here")
        return None

    # Step 3: Create client
    client = anthropic.Anthropic(api_key=api_key)

    try:
        # Step 4: Send a message
        system_prompt = """You are a data extraction assistant.
        Respond ONLY with valid JSON. No extra text, no markdown, no explanation.
        use exactly this structure:
        {
            "summary": "2-3 sentence summary",
            "key_points": ["point 1", "point 2"],
            "sentiment": "positive or negative or neutral",
            "word_count": integer
        }"""
            
        # Step 5 = Send message to LLM    
        response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": text}
                ]
            )

        # Step 6 = Extract JSON
        response_json = extract_json(response.content[0].text)

        return response_json
        
    except anthropic.AuthenticationError:
        print("Error: Invalid API key. Check your ANTHROPIC_API_KEY.")
        return None
    except anthropic.APIConnectionError:
        print("Error: Can't connect to the API. Check your internet.")
        return None
    except anthropic.APIError as e:
        print(f"API error: {e}")
        return None
    
def main():

    sample_text = """Tesla reported strong Q4 2025 results, with revenue reaching $25.7 billion, 
    up 12% year-over-year. The company delivered 495,000 vehicles during the quarter, 
    beating analyst expectations of 473,000. CEO Elon Musk highlighted the growth of 
    the energy storage division, which saw a 150% increase in deployments compared to 
    the previous year.

    However, profit margins continued to face pressure, declining to 17.6% from 19.2% 
    in the same quarter last year. The company attributed the margin compression to 
    aggressive price cuts aimed at maintaining market share amid increasing competition 
    from Chinese EV manufacturers. Several analysts expressed concern about the 
    sustainability of the pricing strategy.

    Despite the margin challenges, investor sentiment remained largely positive, with 
    shares rising 4% in after-hours trading. The company reaffirmed its 2026 delivery 
    target of 2.2 million vehicles and announced plans to begin production at its new 
    Mexico facility by mid-2026."""
    
    
    messy_text_full = """Met this really interesting guy at the conference yesterday — Pablo Santolaya. 
    He's doing his MBA at MIT right now but before that he spent about 5 years 
    running startups in Madrid. Mostly in energy and property from what he told me. 
    Super into AI applications for business operations. Also mentioned he's been 
    getting into prompt engineering lately."""

    messy_text_sparse = """Just had coffee with someone who works in fintech. Really sharp, seems to 
    know a lot about machine learning. Think they're based somewhere in Europe."""

    result = analyze_text(sample_text)

    if result is None:
        print("Error: couldn't get a structured response")
    else:
        #result is a dictionary - use it
        print("=" * 50)
        print("EXERCISE 27 — Text Analysis")
        print("=" * 50)
        print(f"Summary: {result['summary']}\n")
        print(f"Key Points:\n")
        for point in result['key_points']:
            print(f"   - {point}\n")
        print(f"Sentiment: {result['sentiment']}\n")
        print(f"Word count: {result['word_count']}")

    
    result_full = extract_person_info(messy_text_full)

    if result_full is None:
        print("Error: couldn't get a structured response")
    else:
        #result is a dictionary - use it
        print("\n" + "=" * 50)
        print("EXERCISE 28 — Person Extraction (Full)")
        print("=" * 50)
        print(f"Name: {result_full['name']}\n")
        print(f"Job title: {result_full['job_title']}\n")
        print(f"Company: {result_full['company']}\n")
        print(f"Location: {result_full['location']}\n")
        print("Interests:")
        for interest in result_full['interests']:
            print(f"   - {interest}\n")
        print("Fields missing:")
        for miss_field in result_full['fields_missing']:
            print(f"   - {miss_field}\n")

    result_sparse = extract_person_info(messy_text_sparse)

    if result_sparse is None:
        print("Error: couldn't get a structured response")
    else:
        #result is a dictionary - use it
        print("\n" + "=" * 50)
        print("EXERCISE 28 — Person Extraction (Sparse)")
        print("=" * 50)
        print(f"Name: {result_sparse['name']}\n")
        print(f"Job title: {result_sparse['job_title']}\n")
        print(f"Company: {result_sparse['company']}\n")
        print(f"Location: {result_sparse['location']}\n")
        print("Interests:")
        for interest in result_sparse['interests']:
            print(f"   - {interest}\n")
        print("Fields missing:")
        for miss_field in result_sparse['fields_missing']:
            print(f"   - {miss_field}\n")
  
if __name__ == "__main__":
    main()
  
    


