# Import necessary modules and establish logging format and level
from core.core_assistant import CoreAssistant
import logging 
import json
import os

logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d', format='%(levelname)s - %(asctime)s - %(message)s')

class DevOpsAssistant(CoreAssistant):

    def __init__(self):
        super().__init__()  # Initialize parent class attributes

        self.assistant_type = self.dev_ops_engineer  # Set the assistant type to a DevOps engineer

        # Configure the model and API request parameters for better code inference 
        self.gpt_model='gpt-4o'
        self.temperature = 1
        self.response_format=None
        self.max_tokens=None  # Allow the model to return the full response 

    def __articulate_context(self, prompt):
        """
        Constructs a user message for API request including guidelines for adding comments to code.
        """
        user_message = f"""
            Infer logic and write comments for {prompt}. 
            Must be inline with the code. If comments already exist, overwrite
            Write no more than two sentences per function. 
            Keep original formatting
        """
        return user_message
    
    def make_api_request(self, prompt):
        """
        Handles the API request to OpenAI's model with proper error handling.
        """
        user_message = self.__articulate_context(prompt)  # Create user message
        try:
            request = self.pass_instructions(self.assistant_type, user_message)  # Pass instructions to the model
            response = self.get_response(request)  # Obtain response from the model
            logging.debug(f"Response string cleanned, moving on to create a list")
            return response  # Return the model's response
        except Exception as err:
            logging.error(f'Something is wrong, see error: \n {err}')  # Log any errors

    def process_code(self, directory=None):
        """
        Recursively reads all Python files from the given directory, passes them to the API for comment insertion,
        and writes the commented code back to the respective files.
        """
        
        success = False
        # Standard directory tree walk to find .py files
        for root, _, files in os.walk(directory):
            
            # Filter and process only .py files
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)

                    # Read the code from each file
                    with open(file_path, 'r') as f:
                        code = f.read()
                    
                    # Obtain commented code from the API
                    commented_code = self.make_api_request(prompt=code)

                    # Write the commented code back to the file
                    with open(file_path, 'w') as f:
                        f.write(commented_code)

# Create an instance of DevOpsAssistant and process code in the specified directory
assistant = DevOpsAssistant()
directory = './core'
assistant.process_code(directory)