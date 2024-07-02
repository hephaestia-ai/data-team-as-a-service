# Assistants 

This repo contains Data Engineering & Analytics AI assistants constructed using the Open AI API and python library. 

Currently the parent folder, 'core' contains the parent 'CoreAssitant' class which is intended to be a base reference 
for the nasenct 'assistants' sub-directory. CoreAssistant currently only makes a basic API call and returns chat completions messages and metadata. 

The assistants sub-directory passes more context to the parent class and also contains assistant-specific data cleaning operations. For example, the current DataGenerationAssistant() outputs results as a pandas dataframe object. I am leaving this more of a loose definition for now. 