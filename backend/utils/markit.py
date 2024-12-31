import asyncio
from glob import glob
import os
import sys
import warnings
from markitdown import MarkItDown
from openai import OpenAI

directory_path = "Documents/Vie/pdf"  # Directory containing PDF files
output_dir = "markdown"

md = MarkItDown()
os.makedirs(output_dir, exist_ok=True)

async def process_file(file_path):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="Custom system prompt was provided*")

        try:
            # Convert the file to Markdown
            result = md.convert(file_path)

            # Save markdown content to file
            # Get the base filename and add .md extension
            output_filename = os.path.basename(file_path).rsplit('.', 1)[0] + '.md'
            output_path = os.path.join(output_dir, output_filename)
            with open(output_path, "w", encoding="utf-8") as f:
               f.write(result.text_content)

           

            print(f"Successfully processed: {file_path}")
        except Exception as e:
            print(f"Error processing {file_path}: {e}", file=sys.stderr)


async def main():
    # Get all PDF files in the directory
    files = glob(os.path.join(directory_path, "*.*"))

    # Process each file asynchronously
    tasks = [process_file(file_path) for file_path in files]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
