# GenAI-Dictionary
A simple Gen AI based dictionary for student
Ver 1.0 - 6th Nov 2024
- This app is designed as a comprehensive learning tool to support students preparing for spelling bees.
- It provides quick, easy access to essential information about words, including their meanings, pronunciation, etymology, synonyms, and antonyms.
- Additionally, students can save words to build a personal study list, making it a practical resource for efficient vocabulary building.

Key Features:

- Front End: Built using Streamlit for a user-friendly and interactive interface.
- Back End: Powered by LangChain framework, with advanced text generation supported by Llama 2 model for efficiency and control.
- Pronunciation Support: Integrates Google Text-to-Speech (gTTS) to deliver accurate pronunciation of each word, aiding in verbal practice.
This app combines streamlined access to vocabulary details with advanced language tools, offering an all-in-one experience tailored to the unique needs of spelling bee students.

Project Structure

- main_ui.py: Main Streamlit application file that handles the UI and interaction.
- models/: Directory where the Llama2 model is stored.
- services/: Custom modules for logging (logging.py) and running services (actions.py).
- logs/: To staore the logs if enabled
- README.md: This file.
- requirements_dictionaryt.txt

Steps:
- Create a python virtual enviroment and activate it.
- I have used anaconda and VS Code for development
- Go to the folder of your choice
- Clone the Repository: git clone https://github.com/moulaskar/GenAI-Dictionary.git
- cd GenAI-Dictionary
- If you have Python installed
    - Install the requiremets pip install -r requirements_dictionary.txt
- else
    - Install the requiremets pip install -r requirements.txt

- Run the Application: streamlit run main_ui.py

   
Ver 2.0 - 7th Nov 2024
- Reagganged the code
- Added feature to save the file locally by user choice
  
Ver 3.0 - 11th Nov
- Updated Steps in Readme
- Added global variables to automate the process
- updated requirements_dictionary.txt and added requirements.txt
