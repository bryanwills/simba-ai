import aiofiles
import os
import warnings
from pyzerox import zerox
from dotenv import load_dotenv
import asyncio
from langsmith import traceable
import sys
from glob import glob

# Ensure UTF-8 encoding globally
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Load environment variables
load_dotenv()

# Model and directory setup
model = "gpt-4o-mini"
pdf_directory_path = "Documents/Vie/pdf"  # Directory containing PDF files
output_dir = "Markdown"
custom_system_prompt = """Convert the following PDF page to markdown.
Return only the markdown with no explanation text.
Do not exclude any content from the page.
Be careful with big tables. If a table spans multiple pages, reconstruct it as a single table.
"""

# Ensure API key is set
os.environ["OPENAI_API_KEY"] = os.getenv('AS_OPENAI_API_KEY')


@traceable
async def process_pdf(file_path):
    select_pages = None  # Process all pages

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="Custom system prompt was provided*")

        try:
            # Process the current PDF file
            raw_result = await zerox(
                file_path=file_path,
                model=model,
                output_dir=output_dir,
                custom_system_prompt=custom_system_prompt,
                select_pages=select_pages,
            )

            

            print(f"Successfully processed: {file_path}")
        except Exception as e:
            print(f"Error processing {file_path}: {e}", file=sys.stderr)


async def main():
    # Get all PDF files in the directory
    pdf_files = glob(os.path.join(pdf_directory_path, "*.pdf"))

    # Process each file asynchronously
    tasks = [process_pdf(file_path) for file_path in pdf_files]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
