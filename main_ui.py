import sys
import re
import streamlit as st
from streamlit.web import cli as stcli
from streamlit import runtime
from services.logging import Logger
from services.helpers import *
from services.gpt_service import get_word_info
LOGGER = True

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
def process_result(word, result, logger):
    if logger:
        logger.logMsg(word)

    if st.button("Pronounce"):
        pronounce_word(word)

    display_color_result(word, st.session_state[word])

    # save the result
    str_res = create_the_text(word, result)
    try:
        st.download_button("Save", data=str_res, file_name=word)
    except Exception as err:
        st.write(f"Error in saving file e: {err}")
        return None   
    
def main():
    # initialize the logger
    if LOGGER:
        # create logger object
        logger = Logger("log")
    else:
        logger = None

    # create the initial text display(
    initialize_UI()

    # Input section
    word = st.text_input(label="Word")
    # Initialize result in session state to prevent re-fetching
    if word not in st.session_state:
        st.session_state[word] = None

    if word:
        result = get_info(word, logger)
        st.session_state[word] = result
        if result:
            process_result(word, result, logger)
        else:
            st.write("No information available for this word.")

if __name__ == "__main__":
    main()
    
        

