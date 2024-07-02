from core.core_assistant import CoreAssistant
import re
import logging 

logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d', format='%(levelname)s - %(asctime)s - %(message)s')

class DataGenerationAssistant(CoreAssistant):
    """
    Data Generation Assistant
    -------------------------

    An assistant that's sole purpose is to generate data that 
    can be used to either enrich other data, create test or temporary data, 
    or really anything you can think of. 

    Output will contain a python serialized list object
    """

    def __init__(self):
        super().__init__()
        self.assistant_type = self.data_engineer

    def __articulate_context(self, prompt): 
        """
        Constructs a user message for generating data based on the provided prompt.
        Returns the formatted user message as a string.
        """
        user_message = f"""
            Generate data for {prompt} and output as json object. Do not include anything else in output
            Attribute headers must not exceed 4 elements. Return the column or attribute name first
        """
        return user_message    
    
    def get_response_str(self, prompt): 
        """ 
        Makes an API request to OpenAI for generating data based on the prompt and returns the response string.
        Handles and logs any errors during the process.
        """
        user_message = self.__articulate_context(prompt)
        try:
            request = self.pass_instructions(self.assistant_type, user_message)
            response = self.get_response(request)
            response = response.replace('\n', '')
            logging.debug(f"Response string cleanned, moving on to create a list")
            return response
        except Exception as err:
            logging.error(f'Something is wrong, see error: \n {err}')

    def generate_list(self, prompt):
        """
        Generates a Python list of data based on the prompt.
        Processes and cleans the GPT response to ensure it is a valid list.
        """
        output_str = self.get_response_str(prompt)
        assert isinstance(output_str, str), "GPT Response type must be a string"
        output_str = re.sub(r'"', '', output_str)
        output_list = output_str.split(sep=',')
        output_list = [i.strip() for i in output_list] 
        assert isinstance(output_list, list), "Must be a list datatype, something is wrong"
        return output_list

    def create_structured_dataframe(self, data):
        """
        Creates a pandas DataFrame from the given data.
        Constructs the DataFrame with the first 4 elements as headers and the remaining elements as rows.
        """
        import pandas as pd
        structured = []
        for i in range(0, len(data), 4):
            grouped = data[i:i+4] 
            structured.append(grouped)
        return pd.DataFrame(data=structured[1:], columns=[structured[0]])

    def get_response_json(self, prompt):
        """
        Makes an API request to OpenAI for generating data based on the prompt and returns the response JSON.
        Handles and logs any warnings during the process.
        """
        user_message = self.__articulate_context(prompt)
        try:
            request = self.pass_instructions(self.assistant_type, user_message)
            response = self.get_response(request)
            logging.debug(f"Response string cleanned, moving on to create a list")
            return response
        except Exception as err: 
            logging.warn(f"Warning, see issue: {err}")

if __name__=="__main__":
    DataGenerationAssistant()