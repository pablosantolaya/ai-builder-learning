def split_into_chunks(text, chunk_size=500, overlap=50):
    word_list = text.split()
    chunk_list = []
    position = 0

    while position < len(word_list):
        chunk_string = " ".join(word_list[position:position+chunk_size])
        position += chunk_size-overlap
        chunk_list.append(chunk_string)

    return chunk_list

test_text = " ".join([f"word{i}" for i in range(100)])

chunks = split_into_chunks(test_text, chunk_size=30, overlap=5)

for i, chunk in enumerate(chunks):
    words_in_chunk = chunk.split()
    print(f"Chunk {i+1}: {len(words_in_chunk)} words. starts with '{words_in_chunk[0]}', ends with '{words_in_chunk[-1]}'")

total_words_in_chunks = sum(len(chunk.split()) for chunk in chunks)
overlap_words = 5* (len(chunks)-1)
unique_words = total_words_in_chunks - overlap_words
original_words = len(test_text.split())

print(f"Original: {original_words} words")
print(f"Chunks contain: {total_words_in_chunks} words total")
print(f"Minus {overlap_words} overlap words = {unique_words} unique words")
print(f"Match: {unique_words == original_words}")