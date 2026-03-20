import argparse
import os
from file_utils import read_file, save_results
from config import OUTPUT_DIRECTORY
from analyzer_functions import (
    line_count, word_count, character_count,
    sentence_count, average_word_length,
    top_n_word, reading_time
)

def main():
    parser = argparse.ArgumentParser(description="Analyze a text file")
    parser.add_argument("input_file", help="Path to the file to analyze")
    parser.add_argument("--output", help="Path to save results (optional)")

    args = parser.parse_args()

    content = read_file(args.input_file)
    if content is None:
        return
    
    results = {
        "line_count": line_count(content),
        "word_count": word_count(content),
        "char_count": character_count(content),
        "sentence_count": sentence_count(content),
        "avg_word_length": average_word_length(content),
        "top_n_word": top_n_word(content),
        "reading_time": reading_time(content)
    }

    if args.output is None:
        args.output = os.path.join(OUTPUT_DIRECTORY, "results.json")
    
    save_results(results, args.output)

if __name__ == "__main__":
    main()
