# Function to analyze text
import json

def text_analyzer(filename):
    with open(filename, "r") as f: #Read text file in lines
        lines = f.readlines()

    reading_per_minute = 200        # Constants

    line_count = 0                  # Viariables
    word_count = 0
    character_count = 0
    sentence_count = 0
    average_word_length = 0
    word_counter = {}
    reading_time = 0

    line_count = len(lines)

    for line in lines:
        words = line.split()
        word_count += len(words)
        sentence_count += line.count(".") + line.count("?") + line.count("!")
        for word in words:
            character_count += len(word)
            if word in word_counter.keys():
                word_counter[word] += 1
            else:
                word_counter[word] = 1
    
    average_word_length = character_count / word_count
    reading_time = word_count / reading_per_minute

    sorted_words = sorted(word_counter, key=word_counter.get, reverse=True)
    top_5_words = sorted_words[:5]

    return {"lines": line_count, "words": word_count, "characters": character_count, "sentences": sentence_count, "average word len": average_word_length, "top 5 words": top_5_words, "reading estimate": reading_time}

results = text_analyzer("projects/text_analyzer/sample_text.txt")
print(results)

with open("projects/text_analyzer/output/analysis.json","w") as f:
    json.dump(results, f, indent=4)
