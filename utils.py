import os
import tarfile
import openai_wrapper
from log import logger
from datetime import datetime
from models.tailoring_options import TailoringOptions
from config import APPLICANT_NAME

def generate_tex_and_tar(current_time: str, company_name: str, latex_content: str, file_name: str= "resume", folder_name: str="resume"):
    """
    Creates a folder, generates a .tex file inside it, and compresses the folder into a .tar file.

    Parameters:
        file_name (str): The name of the .tex file to create.
        latex_content (str): The LaTeX content to write into the file.
        folder_name (str): The name of the folder to create.
    """
    try:
        # Path of a folder for saving .tex files
        resume_folder_path = f'./CVs/{current_time}_{company_name}'

        # Path of .tar file
        tar_path = f'./CVs/{current_time}_{company_name}'

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

def generate_pdf(company_name: str, tailored_plain_resume: str, tailoring_options: TailoringOptions):
    # Get the current time formatted as YYYY-MM-DD_HH-MM-SS
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Make a folder for each job description to save PDF, .tex, and .tar files of tailored resume.
    os.makedirs(f'./CVs/{current_time}_{company_name}', exist_ok=True)

    latex_compiler_response, latex_code = openai_wrapper.covert_plain_resume_to_latex(
        current_time, company_name, tailored_plain_resume, tailoring_options.ai_model, tailoring_options.resume_template
    )
    # Path to save pdf file of tailored resume
    pdf_path = f'./CVs/{current_time}_{company_name}/{APPLICANT_NAME}_cv.pdf'
    with open(pdf_path, 'wb') as f:
        f.write(latex_compiler_response.content)
    logger.debug(f"Generated resume saved at here: {pdf_path}")
    return {"pdf_path": pdf_path, "latex_code": latex_code}