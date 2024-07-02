class AssistantType: 
    """ 
    Assistant Type 
    --------------

    Pick the type of chat assistant you would like to interact with. 
    Configured by adding assitional attributes. 

    -----
    """
    def __init__(self): 
        # Initialize different types of assistant roles
        self.data_engineer = 'data engineer'
        # Role for data quality related interactions
        self.data_quality_engineer = 'data quality engineer'
        # Role for data analysis related interactions
        self.data_analyst = 'data analyst'
        # Role for dev ops related interactions
        self.dev_ops_engineer = 'dev ops engineer'