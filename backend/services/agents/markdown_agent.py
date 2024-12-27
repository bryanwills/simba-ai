import subprocess
import os

def convert_pdf_to_markdown(pdf_path, output_dir, batch_multiplier=2, max_pages=None, lang='French'):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Build the command for marker_single
    command = [
        'marker_single',
        pdf_path,
        output_dir
    ]

    # Add optional parameters if provided
    if batch_multiplier:
        command.append(f'--batch_multiplier={batch_multiplier}')
    if max_pages:
        command.append(f'--max_pages={max_pages}')
    if lang:
        command.append(f'--langs={lang}')

    # Execute the command
    try:
        subprocess.run(command, check=True)
        print(f'Successfully converted {pdf_path} to Markdown in {output_dir}')
    except subprocess.CalledProcessError as e:
        print(f'Error during conversion: {e}')


def convert_all_pdfs_to_markdown(input_dir, output_dir, workers=4, max_pages=None, lang='French'):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Build the command for marker_single
    command = [
        'marker ',
        input_dir,
        output_dir
    ]

    # Add optional parameters if provided
    if workers:
        command.append(f'--workers={workers}')
    if max_pages:
        command.append(f'--max ={max_pages}')
    

    # Execute the command
    try:
        subprocess.run(command, check=True)
        print(f'Successfully converted pdfs in {input_dir} to Markdown in {output_dir}')
    except subprocess.CalledProcessError as e:
        print(f'Error during conversion: {e}')



# Example usage
pdf_directory_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'documents', 'vie','pdf')
pdf_name = "Fiche Produit LIBERIS Compte.pdf"  # Replace with your PDF file path
pdf_file_path = os.path.join(pdf_directory_path,pdf_name)

input_directory = pdf_directory_path
output_directory = 'markdown'  # Replace with your desired output directory

# convert_pdf_to_markdown(pdf_file_path, output_directory, batch_multiplier=2, max_pages=10, lang='French')
convert_all_pdfs_to_markdown(input_directory, output_directory)
import subprocess
import os

def convert_pdf_to_markdown(pdf_path, output_dir, batch_multiplier=2, max_pages=None, lang='French'):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Build the command for marker_single
    command = [
        'marker_single',
        pdf_path,
        output_dir
    ]

    # Add optional parameters if provided
    if batch_multiplier:
        command.append(f'--batch_multiplier={batch_multiplier}')
    if max_pages:
        command.append(f'--max_pages={max_pages}')
    if lang:
        command.append(f'--langs={lang}')

    # Execute the command
    try:
        subprocess.run(command, check=True)
        print(f'Successfully converted {pdf_path} to Markdown in {output_dir}')
    except subprocess.CalledProcessError as e:
        print(f'Error during conversion: {e}')


def convert_all_pdfs_to_markdown(input_dir, output_dir, workers=4, max_pages=None, lang='French'):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Build the command for marker_single
    command = [
        'marker ',
        input_dir,
        output_dir
    ]

    # Add optional parameters if provided
    if workers:
        command.append(f'--workers={workers}')
    if max_pages:
        command.append(f'--max ={max_pages}')
    

    # Execute the command
    try:
        subprocess.run(command, check=True)
        print(f'Successfully converted pdfs in {input_dir} to Markdown in {output_dir}')
    except subprocess.CalledProcessError as e:
        print(f'Error during conversion: {e}')



# Example usage
pdf_directory_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'documents', 'vie','pdf')
pdf_name = "Fiche Produit LIBERIS Compte.pdf"  # Replace with your PDF file path
pdf_file_path = os.path.join(pdf_directory_path,pdf_name)

input_directory = pdf_directory_path
output_directory = 'markdown'  # Replace with your desired output directory

# convert_pdf_to_markdown(pdf_file_path, output_directory, batch_multiplier=2, max_pages=10, lang='French')
convert_all_pdfs_to_markdown(input_directory, output_directory)