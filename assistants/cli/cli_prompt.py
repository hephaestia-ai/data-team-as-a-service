            
from assistants.data_generation_assistant import DataGenerationAssistant
import argparse 
import logging
import json
import os
import pandas as pd

logging.basicConfig(level=logging.INFO, datefmt="%Y-%m-%d", format="%(levelname)s - %(asctime)s - %(message)s")

def handle_underscores(args):
    # Utility function to replace spaces in the passed prompt string with underscores
    return args.replace(' ', '_')


def handle_files(args):
    # Checks if output directory exists, creates if not, then joins prompt to file path 
    directory = 'mnt/data/'
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_name = handle_underscores(args.run)
    file_path = os.path.join(directory, f'{file_name}.json')
    return file_path, file_name


def pass_arguments_to_data_gen_assistant(args):
    # Command line interface function to pass arguments to DataGenerationAssistant class and save output as JSON 
    file_path, file_name = handle_files(args)

    assistant = DataGenerationAssistant()

    json_object = assistant.get_response_json(prompt=args.run)
    json_data = json.loads(json_object)
    with open(file_path, 'w', encoding='utf-8') as output_json:
        json.dump(json_data, output_json, ensure_ascii=False, indent=4)
    logging.info(f"JSON data has been written to {file_path}")


def run():
    # Parses a prompt from the CLI to the data generation assistant
    parser = argparse.ArgumentParser(description="Pass prompt through the command line to a specific assistant")
    parser.add_argument('-r', '--run', type=str, help='Write the shortened prompt to pass')
    args = parser.parse_args()
    pass_arguments_to_data_gen_assistant(args)