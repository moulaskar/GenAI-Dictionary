'''
THis file will have all the helper functions
'''
import streamlit as st
from gtts import gTTS
from io import BytesIO

def pronounce_word(word):
    audio_data = text_to_speech(word)
    # Button to play the TTS audio
    st.audio(audio_data, format="audio/mp3")
    return

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

def create_the_text(word, result):
    ''' From dictionary create the text'''
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
    


def save_the_result(word, result):
    str_res = create_the_text(word, result)
    try:
        st.download_button("Save", data=str_res, file_name=word)
    except Exception as err:
        st.write(f"Error in saving file e: {err}")
        return None
    
# Function to handle text-to-speech
def text_to_speech(text):
    tts = gTTS(text=text, lang="en", slow=False)
    audio_fp = BytesIO()
    tts.write_to_fp(audio_fp)
    audio_fp.seek(0)  # Move to the start of the BytesIO stream
    return audio_fp  


# save the result in single file
def save_to_file(str_res, base_directory):
    import os
    # Specify the filename you want to save
    file_name = "words.doc"
    file_path = os.path.join(base_directory, file_name)
    
    try:
        # Write the text to the specified file path
        with open(file_path, "a+", encoding='utf-8') as file:
            file.write(str_res)
        st.success(f"File saved successfully at {file_path}")
    except Exception as e:
        st.error(f"Error saving file: {e}")
    return