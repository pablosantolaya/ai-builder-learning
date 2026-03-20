from config import TOP_N_WORDS, READING_PER_MINUTE

def line_count(file_content):
    lines = file_content.split("\n")
    num_lines = len(lines)
    return num_lines

def word_count(file_content):
    words = file_content.split()
    num_words = len(words)
    return num_words

def character_count(file_content):
    num_characters = len(file_content)
    return num_characters

def sentence_count(file_content):
    num_sentence = file_content.count(".") + file_content.count("!") + file_content.count("?")
    return num_sentence

def average_word_length(file_content):
    words = file_content.split()
    num_words = len(words)
    
    if num_words == 0:
        return 0
    
    total_char = 0    
    for word in words:
        total_char += len(word)
    

    
    word_length = total_char / num_words

    return word_length

def top_n_word(file_content):
    word_counter = {}
    words = file_content.split()
    for word in words:
        if word in word_counter.keys():
            word_counter[word] += 1
        else:
            word_counter[word] = 1
    
    sorted_words = sorted(word_counter, key=word_counter.get, reverse=True)
    top_n = sorted_words[:TOP_N_WORDS]

    return top_n
    
def reading_time(file_content):
    words = file_content.split()
    num_words = len(words)
    read_time = num_words / READING_PER_MINUTE

    return read_time