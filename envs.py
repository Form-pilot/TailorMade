from os import getenv
from dotenv import load_dotenv
from log import logger

# Load environment variables from .env file
load_dotenv()

OPEN_AI_KEY = getenv("OPEN_AI_KEY")  # Put your open AI key here
GMAIL_APP_PASSWORD = getenv("GMAIL_APP_PASSWORD")  # Put your gmail app password here
ADD_GDRIVE_ZAP_URL = getenv("ADD_GDRIVE_ZAP_URL")  # Put zappier webhook workflow here, This webhook uploads the file to GDrive
LaTeX_COMPILER_URL = "https://texlive2020.latexonline.cc/compile?command=pdflatex&text="
# LaTeX_COMPILER_URL = "https://latexonline.cc/compile?command=xelatex&text="
LaTeX_COMPILER_URL2 = "https://latexonline.cc/data?target=resume/AliAf.tex&force=true&command=pdflatex"

import os
import tarfile

def create_tex_file(file_name, latex_content, folder_name):
    """
    Creates a folder, generates a .tex file inside it, and compresses the folder into a .tar file.

    Parameters:
        file_name (str): The name of the .tex file to create.
        latex_content (str): The LaTeX content to write into the file.
        folder_name (str): The name of the folder to create.
    """
    try:
        # Ensure the folder exists
        os.makedirs(folder_name, exist_ok=True)

        # Full path for the .tex file
        tex_file_path = os.path.join(folder_name, file_name)

        # Ensure the file name ends with .tex
        if not tex_file_path.endswith(".tex"):
            tex_file_path += ".tex"

        # Write the LaTeX content into the file
        with open(tex_file_path, "w", encoding="utf-8") as tex_file:
            tex_file.write(latex_content)

        logger.debug(f"File '{tex_file_path}' created successfully.")

        # Compress the folder into a .tar file
        tar_file_name = f"{folder_name}.tar"
        with tarfile.open(tar_file_name, "w") as tar:
            tar.add(folder_name, arcname=os.path.basename(folder_name))

        logger.debug(f"Folder '{folder_name}' compressed into '{tar_file_name}'.")
    except Exception as e:
        logger.debug(f"An error occurred: {e}")