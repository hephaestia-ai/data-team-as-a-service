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
        Articulate Context 
        ------------------
        Constructs a user message that articulates context to the ChatGPT user role

        Passes 'prompt' attribute specified by user to the message string
        Returns user message as string to be referenced by in the instruction request
        """

        user_message = f"""
            Generate data for {prompt} and output as json object. Do not include anything else in output
            Attribute headers must not exceed 4 elements. Return the column or attribute name first
        """
        return user_message    
    
    def get_response_str(self, prompt): 
        """ 
        Independently makes request to OpenAI API, calls the private context method and passes 
        information to the parent method to make the chat completion request. 

        If the 'get_str' method is called, assume the output should be a python list data type
        Prompt must be provided by user. 

        Works independently from make request in case we would just like to get the message data. 
        """
        user_message = self.__articulate_context(prompt)
        try:
            # This is where we call the parent classes pass_instructions method
            # to make an API request to OpenAI 
            request = self.pass_instructions(self.assistant_type, user_message)
            response = self.get_response(request)

            # Process any new line characters
            response = response.replace('\n', '')
            logging.debug(f"Response string cleanned, moving on to create a list")
            return response
        except Exception as err:
            logging.error(f'Something is wrong, see error: \n {err}')

    def generate_list(self, prompt):
        """
        Generate List Method
        ----------------
        Returns a python list object containing data from the prompt

        Processes data from the private '__get_response_str()' method as a python list.
        Removes the GPT output brackets, then removes the single quotation mark, replace with nothing.
        Last step splits the string at the comma sep (converting it to a list) and returns the final list.

        Usage:: 

            >>> prompt = "10 flower names"
            >>> assistant = DataGenerationAssistant()
            >>> data = assistant.generate_list(prompt=prompt)
        
        -----
        """

        output_str = self.get_response_str(prompt)
        assert isinstance(output_str, str), "GPT Response type must be a string"

        output_str = re.sub(r'"', '', output_str)
        output_list = output_str.split(sep=',')
        output_list = [i.strip() for i in output_list] # clean whitespace if exists

        assert isinstance(output_list, list), "Must be a list datatype, something is wrong"
        return output_list

    def create_structured_dataframe(self, data):
        """
        Create Structured DataFrame 
        ---------------------------

        Using pandas, iterate over the response data from the API call and append to a structured list.
        Then selects the first 4 list iterations (headers) considering them as column headers.
        Every '4' records thereafter considered dataframe values.

        Assumes the output string / response respects the provided prompt. 
        """

        import pandas as pd

        structured = []
        for i in range(0, len(data), 4):
            grouped = data[i:i+4] 
            structured.append(grouped)

        return pd.DataFrame(data=structured[1:], columns=[structured[0]])


    def get_response_json(self, prompt):

        user_message = self.__articulate_context(prompt)
        try:
            # This is where we call the parent classes pass_instructions method
            # to make an API request to OpenAI 
            request = self.pass_instructions(self.assistant_type, user_message)
            response = self.get_response(request)
            logging.debug(f"Response string cleanned, moving on to create a list")
            return response
        except Exception as err: 
            logging.warn(f"Warning, see issue: {err}")

if __name__=="__main__":
    DataGenerationAssistant()
