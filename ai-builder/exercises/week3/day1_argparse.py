import argparse

def main():

    parser = argparse.ArgumentParser(description="Analyze a text file")
    parser.add_argument("input_file", help="Path to the file to analyze")
    parser.add_argument("--output", help="Path to save results (optional)")


    args = parser.parse_args()

    try:
        with open(args.input_file,"r") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"File not found. Please ensure you provided the correct path and try again")
        return
    
    if args.output is None:
        print(content)
    else:
        with open(args.output, "w") as f:
            f.write(content)

if __name__ == "__main__":
    main()