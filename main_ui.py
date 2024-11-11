import sys
import re
import os
import streamlit as st
from streamlit.web import cli as stcli
from streamlit import runtime
from services.logging import Logger
from services.helpers import *
from services.gpt_service import get_word_info
from huggingface_hub import hf_hub_download
from langchain_community.llms import LlamaCpp

LOGGER = True
SAVE_TO_SINGLE_FILE = False

# Pre-requisites and global variables
# Create a logger object
# Initialize Streamlit and display a loading message
placeholder = st.empty()
placeholder.text("Preparing the application, Please wait...")
logger = Logger("log") if LOGGER else None

if not os.path.exists("logs"):
    os.makedirs("logs")  # Create the 'log' directory

if not os.path.exists("models"):
    os.makedirs("models")  # Create the 'log' directory
    # Replace with the repo_id of the model and the specific filename
    repo_id = "TheBloke/Llama-2-7B-Chat-GGUF"
    filename = "llama-2-7b-chat.Q4_K_S.gguf"

    # Download the model file
    model_path = hf_hub_download(repo_id=repo_id, filename=filename, local_dir="models")
llm = LlamaCpp(
            model_path="models/llama-2-7b-chat.Q4_K_S.gguf",
            n_gpu_layers=40,
            n_batch=512,  # Batch size for model processing
            verbose=False,  # Enable detailed logging for debugging
        )
    

placeholder.text("")

def initialize_UI():
    # Streamlit UI setup
    st.title("Generative AI Dictionary")
    st.write("Enter a word to get its definition, example sentence, etymology, synonyms, and antonyms.")

def get_info(word, logger):
    # Fetch information using the GPT service function
    logger.logMsg("get_info: getting the result")
    result = get_word_info(word, llm, logger)
    return result


# Display fetched word information
def process_result(word, result):
    if logger:
        msg = f'Processing result in function process_result for word {word}'
        logger.logMsg(msg)

    # Button to Pronounce
    if st.button("Pronounce"):
        pronounce_word(word)

    # display result
    display_color_result(word, st.session_state[word])

    
   
    # Button to save
    if SAVE_TO_SINGLE_FILE:
            import os
            str_res = create_the_text(word, result)
            if st.button("Save in Single File"):
                base_directory = os.path.dirname(__file__)
                save_to_file(str_res, base_directory)
                return
    else:
        try:
            str_res = create_the_text(word, result)
            st.download_button("Save", data=str_res, file_name=word)
        except Exception as err:
            st.write(f"Error in saving file e: {err}")
            return None   
    return
    
def get_getAI_result():
    # Input section
    word = st.text_input(label="Word")
    # Initialize result in session state to prevent re-fetching
    if word not in st.session_state:
        st.session_state[word] = None
        
    result = st.session_state[word]
    if not st.session_state[word]:
        result = get_info(word, logger)
        st.session_state[word] = result
    return word, result

def initialize():
    st.title("Generative AI Dictionary")
    st.write("Enter a word to get its definition, example sentence, etymology, synonyms, and antonyms.")
    return 


if __name__ == "__main__":
    initialize()
    word, result = get_getAI_result()
    if word and result:
        process_result(word, result)

    
    
        

