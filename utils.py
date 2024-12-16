import os
import tarfile
from log import logger

def generate_tex_and_tar(company_name: str, latex_content: str, file_name: str= "resume", folder_name: str="resume"):
    """
    Creates a folder, generates a .tex file inside it, and compresses the folder into a .tar file.

    Parameters:
        file_name (str): The name of the .tex file to create.
        latex_content (str): The LaTeX content to write into the file.
        folder_name (str): The name of the folder to create.
    """
    try:
        # Path of a folder for saving .tex files
        resume_folder_path = f'./CVs/{company_name}/{folder_name}'

        # Path of .tar file
        tar_path = f'./CVs/{company_name}'


        # Ensure the folder exists
        os.makedirs(resume_folder_path, exist_ok=True)

        # Full path for the .tex file
        tex_file_path = os.path.join(resume_folder_path, file_name)

        # Ensure the file name ends with .tex
        if not tex_file_path.endswith(".tex"):
            tex_file_path += ".tex"

        # Write the LaTeX content into the file
        with open(tex_file_path, "w", encoding="utf-8") as tex_file:
            tex_file.write(latex_content)

        logger.debug(f"File '{tex_file_path}' created successfully.")

        # Compress the folder into a .tar file
        tar_file_name = f"{folder_name}.tar"

        # Full path of .tar folder
        tar_folder_path = os.path.join(tar_path, tar_file_name)
        with tarfile.open(tar_folder_path, "w") as tar:
            tar.add(resume_folder_path, arcname='resume')
        return (os.path.relpath(tar_folder_path))
    except Exception as e:
        logger.debug(f"An error occurred: {e}")