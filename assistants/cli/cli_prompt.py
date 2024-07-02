from assistants.data_generation_assistant import DataGenerationAssistant
import argparse 
import logging
import json
import os
import pandas as pd

logging.basicConfig(level=logging.INFO, datefmt="%Y-%m-%d", format="%(levelname)s - %(asctime)s - %(message)s")

def handle_underscores(args):
    """
    Utility function to replace GPT prompt string with 
    underscores to automate loading to biguqery 
    """

    return args.replace(' ', '_')


def handle_files(args):
    """
    Checks to see if output mnt/data sub-dir exists, 
    then joins to file path and cleans the prompt passed via CLI
    """

    directory = 'mnt/data/'
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_name = handle_underscores(args.run)
    file_path = os.path.join(directory, f'{file_name}.json')
    return file_path, file_name


def pass_arguments_to_data_gen_assistant(args):
    """
    Create command line interface function that passes the args to the 
    DataGenerationAssistant class

    We're using OpenAI's response format output because bigquery has the ability 
    to read a json object directly. 

    prompt --run='5 indoor houseplants'
    """

    file_path, file_name = handle_files(args)

    assistant = DataGenerationAssistant()

    json_object = assistant.get_response_json(prompt=args.run)
    json_data = json.loads(json_object)
    with open(file_path, 'w', encoding='utf-8') as output_json:
        json.dump(json_data, output_json, ensure_ascii=False, indent=4)
    logging.info(f"JSON data has been written to {file_path}")


def run():
    """
    Parses a prompt from the CLI to a data generation assistant.
     
    Usage::
        
        % prompt --run='5 indoor houseplants'

    """

    # Establish initial parser object
    parser = argparse.ArgumentParser(description="Pass prompt through the command line to a specific assistant")
    parser.add_argument('-r', '--run', type=str, help='Write the shortened prompt to pass')
    # Initialize 'args' with the arguments established in step 2
    # Pass as parameter to the DataGenerationAssistant 
    args = parser.parse_args()
    pass_arguments_to_data_gen_assistant(args)