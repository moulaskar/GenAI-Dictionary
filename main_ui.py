import sys
import re
import streamlit as st
from streamlit.web import cli as stcli
from streamlit import runtime
from services.logging import Logger
from services.helpers import *
from services.gpt_service import get_word_info
LOGGER = True
SAVE_TO_SINGLE_FILE = True

# Create a logger object
if LOGGER:
    # create logger object
    logger = Logger("log")
else:
    logger = None

def initialize_UI():
    # Streamlit UI setup
    st.title("Generative AI Dictionary")
    st.write("Enter a word to get its definition, example sentence, etymology, synonyms, and antonyms.")

def get_info(word, logger):
    # Fetch information using the GPT service function
    logger.logMsg("get_info: getting the result")
    result = get_word_info(word, logger)
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

    
    
        

