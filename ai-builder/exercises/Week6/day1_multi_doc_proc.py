import os

BASE_DIR = os.path.dirname(__file__)

def load_documents(folder_path):
    txt_files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]
    files_list = []
    for name in txt_files:
        file = {}
        with open(os.path.join(folder_path, name), "r") as f:
            file_content = f.read()
        file["filename"] = name
        file["content"] = file_content
        file["word_count"] = len(file_content.split())
        files_list.append(file)
    
    return files_list

def build_synthesis_prompt(documents):
    prompt = "Here are summaries from multiple documents:\n"
    for document in documents:
        prompt += f"--- Document: {document['filename']} ---\n"
        prompt += f"{document['content']}\n"
    prompt += "Based on these documents, identify the common themes, key differences, and any contradictions between them."
    
    return prompt

def check_prompt_size(prompt, max_words=3000):
    words_prompt = len(prompt.split())
    return words_prompt, words_prompt <= max_words

docs_folder = os.path.join(BASE_DIR, "test_docs")
os.makedirs(docs_folder, exist_ok=True)

with open(os.path.join(docs_folder,"notes.txt"),"w") as f:
    f.write("Machine learning models require large amounts of training data to perform well. The quality of the data matters as much as the quantity. Poorly labeled data leads to unreliable predictions, even with sophisticated algorithms. Data cleaning is often the most time-consuming part of any ML project.")

with open(os.path.join(docs_folder,"report.txt"),"w") as f:
    f.write("The energy sector is undergoing a rapid transformation driven by renewable technologies. Solar panel costs have dropped significantly over the past decade, making distributed generation viable for commercial buildings. Battery storage remains the key bottleneck, but recent advances in lithium-iron-phosphate chemistry are promising. Several startups are exploring vehicle-to-grid solutions that could reshape demand management.")

with open(os.path.join(docs_folder,"summary.txt"),"w") as f:
    f.write("Artificial intelligence is increasingly used in back-office operations to automate repetitive tasks. Invoice processing, contract review, and customer onboarding are common early targets for automation. Companies that start with well-documented processes see faster ROI from AI implementation. The biggest challenge is rarely the technology itself but rather change management and employee adoption.")

content = load_documents(docs_folder)
prompt = build_synthesis_prompt(content)

print(prompt)