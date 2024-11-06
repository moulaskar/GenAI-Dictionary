import wandb
import logging
import os
from datetime import datetime
os.environ["WANDB_MODE"] = "offline"
class WandbLogger:
    def __init__(self, project_name="dictionary"):
        # Initialize W&B with the project name
        wandb.init(project=project_name)
        wandb.config.update({"app": "Generative AI Dictionary"})
        print("W&B initialized with project:", project_name)

        # Set up logging to file and console
        now = datetime.now()
        timestmp = now.strftime("%y%m%d%H%M%S")
        logFilename = timestmp + "_dictionary.log" 
        log_file_path = os.path.join("logs", logFilename)
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
        
        # Configure logging
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler(log_file_path),
                logging.StreamHandler()
            ]
        )

    def log_input(self, word):
        # Log each word query
        wandb.log({"query_word": word})
        logging.info(f"Logged word: {word}")

    def logger_log(self, msg):
        # add other messages
        wandb.log({"debug": msg})
        logging.info({"debug: ", msg})
        return 


    def log_response(self, word, response):
        # Log the API response details
        
        wandb.log({
            "word": word,
            "definition": response.get("definition", "N/A"),
            "example_sentence": response.get("example_sentence", "N/A"),
            "etymology": response.get("etymology", "N/A"),
            "synonyms": ", ".join(response.get("synonyms", [])),
            "antonyms": ", ".join(response.get("antonyms", [])),
        })
        logging.info(f"Logged response for word: {word}")

    def alert_issue(self, message):
        # Create an alert for specific issues
        wandb.alert(title="Dictionary App Issue", text=message)
        logging.error(f"Alert sent: {message}")
