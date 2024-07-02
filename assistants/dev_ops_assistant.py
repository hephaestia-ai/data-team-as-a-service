from core.core_assistant import CoreAssistant
# import re
import logging 

logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d', format='%(levelname)s - %(asctime)s - %(message)s')


class DevOpsAssistant(CoreAssistant):

    def __init__(self):
        super().__init__()

        self.assistant_type = self.dev_ops_engineer