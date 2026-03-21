import argparse
from config import OUTPUT_DIRECTORY
from file_utils import read_file, save_json_results, save_text_report
from processor import process_transcript
from datetime import datetime


def main():
    print("Script started")
    
    parser = argparse.ArgumentParser(description="Analyze a text file")
    parser.add_argument("input_file", help="Path to the file")
    parser.add_argument("--output", default=OUTPUT_DIRECTORY, help="Path to save results")

    args = parser.parse_args()

    file = read_file(args.input_file)
    print(f"File read: {file is not None}")
    if file is None:
        return
    
    result = process_transcript(file)
    print(f"Result: {result is not None}")
    if result is None:
        return
    
    print(f"Parsed data keys: {result['parsed_data'].keys()}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    save_json_results(result, args.output, timestamp)
    save_text_report(result["parsed_data"], args.output, timestamp)

if __name__ == "__main__":
    main()