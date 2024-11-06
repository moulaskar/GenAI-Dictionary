#from langchain import LLMChain
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers
import torch
import re
from services.wandb_logger import WandbLogger
import pyttsx3
from langchain_google_community import TextToSpeechTool
from gtts import gTTS
from io import BytesIO
LOG = False

# Load the LLaMA 3 model and tokenizer
model_name = "models/llama-2-7b-chat.Q4_K_S.gguf"  # Update this path to your local LLaMA 3 model
llm = CTransformers(model=model_name, model_type='gpt2')

# logger 
if LOG:
    logger = WandbLogger()

# Define a prompt template for querying the model
# Adjust the prompt to include instructions for labeling each section

prompt_template = PromptTemplate(
    template=(
        "Provide details about the word '{word}' in English and in the following format:\n"
        "- Definition: \n"
        "- Example sentence: \n"
        "- Etymology: \n"
        "- Synonyms: \n"
        "- Antonyms: \n\n"
        "Please do not add any information or comments after the 'Antonyms' section."
        
    ),
    input_variables=["word"],
)

# Function to handle text-to-speech
def text_to_speech(text):
    tts = gTTS(text=text, lang="en", slow=False)
    audio_fp = BytesIO()
    tts.write_to_fp(audio_fp)
    audio_fp.seek(0)  # Move to the start of the BytesIO stream
    return audio_fp

def get_word_info(word, logger):
    
    try:
        # Create a LangChain LLMChain to manage prompt interaction
        llm_chain = LLMChain(llm=llm, prompt=prompt_template)

        # Run the chain to generate the response
        response = llm_chain.run({"word": word})

        logger.logMsg(response)
        # Extract relevant details based on keywords
        result = {
            "definition": extract_section(response, "Definition", "Example sentence"),
            "example_sentence": extract_section(response, "Example sentence", "Etymology"),
            "etymology": extract_section(response, "Etymology", "Synonyms"),
            "synonyms": extract_section(response, "Synonyms", "Antonyms"),
            "antonyms": extract_section(response, "Antonyms", None),
        }

        logger.logMsg(result)
        return result
    except Exception as err:
        return None
    

def extract_section(text: str, start_section: str, end_section: str) -> str:
    """
    Extracts a section of text from a given text based on the start and end markers.

    Args:
    - text (str): The text from which to extract the section.
    - start_marker (str): The starting point to indicate where to begin extraction.
    - end_marker (str): The ending point to indicate where to end extraction.

    Returns:
    - str: The extracted section of text if start and end markers are found, otherwise None.
    """
    pattern_text = None
    if start_section != "Antonyms":
        pattern = rf"{start_section}:\s*(.*?)(?=\n{end_section}:)"
        match = re.search(pattern, text, re.DOTALL)
        if match:
            pattern_text = match.group(1).strip()
            if start_section == "Synonyms":
                list_words = [line.strip('* ').strip() for line in pattern_text.splitlines() if line.strip()]
                pattern_text = ", ".join(list_words)
    else:
        
        #match = re.search(r"Antonyms:\s*((?:\*\s\w+\n?)+)", text)
        match = re.search(r"Antonyms:\s*(.*)", text)
        # Extract and clean the result if found
        if match:
            list_words = [item.strip('* ') for item in match.group(1).strip().splitlines()]
            pattern_text = ", ".join(list_words)
    return pattern_text


