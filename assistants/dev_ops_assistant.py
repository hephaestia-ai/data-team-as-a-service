from core.core_assistant import CoreAssistant
import logging 
import json

logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d', format='%(levelname)s - %(asctime)s - %(message)s')


class DevOpsAssistant(CoreAssistant):

    def __init__(self):
        super().__init__()

        self.assistant_type = self.dev_ops_engineer

        # For reading / writing to code files we need the model to make better inferences
        # We can adjust the parent class settings here:
        self.gpt_model='gpt-4o'
        self.temperature = 1
        self.response_format=None
        self.max_tokens=None # To get full response, set to None 

    def __articulate_context(self, prompt):
        """
        In this case prompt should be a file read as python code
        """
        user_message = f"""
            Infer logic and write comments for {prompt}. 
            Must be inline with the code. If comments already exist, overwrite
            Write no more than two sentences per function. 
            Keep original formatting
        """
        return user_message
    
    def make_api_request(self, prompt):
        
        user_message = self.__articulate_context(prompt)
        try:
            # This is where we call the parent classes pass_instructions method
            # to make an API request to OpenAI 
            request = self.pass_instructions(self.assistant_type, user_message)
            response = self.get_response(request)

            # Process any new line characters
            # response = response.replace('\n', '')
            logging.debug(f"Response string cleanned, moving on to create a list")
            return response
        except Exception as err:
            logging.error(f'Something is wrong, see error: \n {err}')


with open('/Users/teraearlywine/Earlywine-Data-Co/assistants/assistants/data_generation_assistant.py', 'r', newline='') as file: 
    prompt = file.read()

assistant = DevOpsAssistant()
response = assistant.make_api_request(prompt)
print(response)