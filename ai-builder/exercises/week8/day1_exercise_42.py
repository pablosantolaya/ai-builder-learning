import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

messages_list = []
while True:
    user_input = input("You: ")
    
    if user_input == "quit":
        break

    messages_list.append(
        {
            "role": "user",
            "content": user_input
        }
    )
                          
    response = client.messages.create(
        model = "claude-haiku-4-5-20251001",
        max_tokens = 2048,
        system = "You are an LLM chat bot, helping users with whatever questions the may have",
        messages = messages_list       
    )

    print(response.content[0].text)

    messages_list.append(
        {
            "role": "assistant",
            "content": response.content[0].text
        }
    )

print(f"Total messages in history: {len(messages_list)}")
