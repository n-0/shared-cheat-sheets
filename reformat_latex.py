import re
import sys
import argparse
from pathlib import Path

def convert_latex_delimiters(content):
    # 1. Handle Display Math: $$ ... $$ -> \[ ... \]
    # Using re.DOTALL to ensure it catches multi-line display math
    content = re.sub(r'\$\$(.*?)\$\$', r'\\\[ \1 \\\]', content, flags=re.DOTALL)

    # 2. Handle Inline Math: $ ... $ -> \( ... \)
    # We use a non-greedy match to ensure we don't accidentally grab everything 
    # between the start of one formula and the end of another.
    content = re.sub(r'(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)', r'\\( \1 \\)', content)

    return content

def main():
    parser = argparse.ArgumentParser(description="Convert LaTeX math delimiters to modern syntax.")
    parser.add_argument("input_file", help="Path to the .tex file")
    
    args = parser.parse_args()
    input_path = Path(args.input_file)

    if not input_path.exists():
        print(f"Error: File '{args.input_file}' not found.")
        sys.exit(1)

    # Read the original file
    with open(input_path, 'r', encoding='utf-8') as f:
        original_content = f.read()

    # Process content
    parsed_content = convert_latex_delimiters(original_content)

    # Define new filename: original_name_parsed.tex
    new_filename = f"{input_path.stem}_parsed{input_path.suffix}"
    output_path = input_path.parent / new_filename

    # Write the new file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(parsed_content)

    print(f"Success! Processed file saved as: {output_path}")

if __name__ == "__main__":
    main()
