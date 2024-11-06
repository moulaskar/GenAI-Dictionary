import streamlit as st
from services.gpt_service import get_word_info, text_to_speech
from services.logging import Logger

# create logger object
logger = Logger("log")

# Streamlit UI setup
st.title("Generative AI Dictionary")
st.write("Enter a word to get its definition, example sentence, etymology, synonyms, and antonyms.")

# Input section
word = st.text_input("Word:", key='input_word')
# Initialize result in session state to prevent re-fetching
if word not in st.session_state:
    st.session_state[word] = None

def get_info(word):
    # Fetch information using the GPT service function
    result = get_word_info(word, logger)
    #st.write(result)
    if result:
        st.session_state[word] = result


def pronounce_word(word):
    audio_data = text_to_speech(word)
    # Button to play the TTS audio
    st.audio(audio_data, format="audio/mp3")
    return

    #return result
def create_the_text(word):
    ''' From dictionary create the text'''
    result = st.session_state[word]
    try:
        str = ""
        str = f"{word.capitalize()}" + '\n\n'
        if result["definition"]:
            str = str + "Definition" + "\n" + result["definition"] + '\n\n'
        else: 
            str = str + "Definition" + "\n" + '\n\n'
        
        if result["example_sentence"]:
            str = str + "Example Sentence\n" + result["example_sentence"] + '\n\n'
        else:
            str = str + "Example Sentence\n" + '\n\n'

        if result["etymology"]:
            str = str + "Etymology\n" + result["etymology"] + '\n\n'
        else:
             str = str + "Etymology\n" + '\n\n'

        if result["synonyms"]:
            str = str + "Synonyms\n" + result["synonyms"] + '\n\n'
        if result["antonyms"]:
            str = str + "Antonyms\n" + result["antonyms"] + '\n\n'
            str = str + "****************************************\n\n"
        return str
    except Exception as err:
        st.write(f"Error e: {err}")
        return None


def save_the_result(word):
    str_res = create_the_text(word)
    try:
        st.download_button("Save", data=str_res, file_name=word)
    except Exception as err:
        st.write(f"Error in saving file e: {err}")
        return None
    


def colored_output(result, key, bg, txt_col):
    # Style definition text with a light green background and custom color
    definition_text = result.get(key, "Not available")
    st.markdown(
        f"<div style='background-color: {bg}; padding: 10px; border-radius: 5px; color: {txt_col}4;'>{definition_text}</div>",
        unsafe_allow_html=True
    )



def display_color_result(word, result):
    # Display the results
    st.subheader(word.title())
    st.subheader("Definition")
    colored_output(result, "definition", "#FFF9CC", " #666600")

    st.subheader("Example Sentence")
    colored_output(result, "example_sentence", "#d4edda", " #155724")

    st.subheader("Etymology")
    colored_output(result, "etymology", "#FFE5CC", " #CC5500")

    st.subheader("Synonyms")
    colored_output(result, "synonyms", "#E6CCFF", " #4B0082")

    st.subheader("Antonyms")
    colored_output(result, "antonyms", "#FFCCCC", " #990000")
    return
    

def display_result(word, result):
    # Display the results
    st.subheader(word.title())

    st.subheader("Definition")
    st.write(result.get("definition", "Not available"))

    st.subheader("Example Sentence")
    st.write(result.get("example_sentence", "Not available"))

    st.subheader("Etymology")
    st.write(result.get("etymology", "Not available"))

    st.subheader("Synonyms")
    st.write(result.get("synonyms", "Not available"))

    st.subheader("Antonyms")
    st.write(result.get("antonyms", "Not available"))
    return

# Display fetched word information
if word:

    logger.logMsg(word)
    # Run get_info only if data is not already present in session state
    #if st.session_state[word] is None:
    if not st.session_state[word]:
        get_info(word)

    if st.session_state[word]:
        if st.button("Pronounce"):
            pronounce_word(word)
    
    # Display the fetched result from session state
    if st.session_state[word]:
        is_checked = st.checkbox("Remove Color")
        result = st.session_state[word]
        
        if not is_checked:
            display_color_result(word, result)
        else:
            display_result(word, result)
    else:
        st.write("No information available for this word.")

    audio_data = text_to_speech(word)
    # Button to play the TTS audio

    # save the file as text
    if st.session_state[word]:
        save_the_result(word)
        

