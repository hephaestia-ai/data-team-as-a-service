from core.assistant_type import AssistantType
import logging 

logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d', format='%(levelname)s - %(message)s')

class CoreAssistant(AssistantType):
    """
    Assistant
    ----------
        Configuration and initialization of the OpenAI GPT model.
        Will be used as base class for future system / user message iterations.

    Methods
    -------
        get_chat_response: str


    Documentation
    -------------

    + https://github.com/openai/openai-python
    + https://platform.openai.com/docs/libraries/python-library
    + https://cookbook.openai.com/examples/reproducible_outputs_with_the_seed_parameter

    """

    def __init__(self):
        # Initializes AssistantType Parent Class, allows for dynamic role selection
        super().__init__() 
        from openai import OpenAI

        self.gpt_client = OpenAI()  # Setting up the OpenAI client instance
        self.gpt_model = "gpt-4-turbo"  # GPT model specification
        self.temperature = 0.02  # Model temperature for response variability
        self.max_tokens = 210  # Maximum tokens per response
        self.response_format={"type": "json_object"}  # Response format configuration
        self.seed=1  # Seed value for deterministic outputs

    def _parse_usage_stats(self, request):
        """
        Helper method designed to assist with parsing usage stats from the Open AI API response.
        Not intended for public use.
        """
        sys_fingerprint = request.system_fingerprint
        
        usage_stats = request.usage
        completion_cost = usage_stats.completion_tokens
        prompt_cost = usage_stats.prompt_tokens
        total_cost = usage_stats.total_tokens
        
        logging.info(f"System fingerprint (for determinism): {sys_fingerprint}")
        logging.info(f"API Usage Stats **** completion_tokens: {completion_cost}, prompt_tokens: {prompt_cost}, total_tokens: {total_cost} **** ")
        logging.info(f"Model Used: {request.model}")
        logging.info(f"Request created @ {request.created}")



    def pass_instructions(self, assistant_type, prompt):
        """
        Parameters
        ----------
            user_request: string
                provde the instructions to the AI for inference

        Usage::

            >>> user_request = 'Create deterministic sql assertions for any of the following code. Assume it's SQL: {}'
            >>> assistant = CoreAssistant()
            >>> assistant.pass_instructions(assistant_type, user_request)

        -----
        """

        # Send a request to the OpenAI GPT model using chat completion
        chat_completion = self.gpt_client.chat.completions.create(
            messages=[
                {"role": "system", "content": f"you are a helpful {assistant_type} assistant"},
                {"role": "user", "content": "The response should contain no chat message, commentary, additional text, backticks or code (thank you)"},
                {"role": "user", "content": f"{prompt}"},
            ],
            model=self.gpt_model,
            response_format=self.response_format,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            top_p=1, # Highly predictable output
            seed=self.seed 
        )
        return chat_completion

    def get_response(self, request):
        """
        Passes the chat completions request through the class message access point.
        The request parameter being all OpenAI related details such as token cost, 
        deterministic UUID etc.
        
        :param request: 
        :return: 
            generated_data: parsed out message content from the open AI response
        """

        # Parse usage stats for information
        self._parse_usage_stats(request)

        # Process and return message content from request choices
        response = request.choices[0].message.content
        return response

if __name__ == "__main__":
    CoreAssistant()