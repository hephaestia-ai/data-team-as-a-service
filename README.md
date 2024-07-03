# Data Team as a Service (Taster)

Welcome to the Earlywine-Data-Co/data-team-as-a-service *taster* repository!

Yep - you guessed it. There's more to come. While the Grapes are fermenting, we thought we'd leave the open source community with a few things to focus on. 

1. data generation and metadata enrichment is not that hard with the right question
2. code commenting can be automated, for everything. 

Where this is going...

Project Overview: Data Team As A Service (DTAAS)

This repository houses the prototype project Data Team As A Service (DTAAS), developed using the OpenAI API library. The goal of DTAAS is to streamline and automate some of the more repetitive tasks that data analysts and data engineers typically face. Tasks like writing basic data quality checks for 500+ tables, scraping websites for detailed information, or even generating lower-level code comments. Ambitiously, the ultimate goal is to use AI to handle the dev-ops side of data engineering.

### Assistants

The repository currently features two assistants:


+ Data Generation Assistant:
    + This assistant is nearly 95% deterministic and can generate any data from a simple prompt passed through the CLI.
    + The output is structured as a pandas DataFrame.
+ Dev-Ops Assistant:
    + This assistant recursively searches a given directory and adds in-line comments to every single .py file, preserving the original structure of the code.

_Future Development_

The next planned assistant will:

+ Recursively read any SQL and create a suite of DBMS constraint checks.
+ Infer the business logic and cardinality from the SQL.



Note: The code for the next assistant might not be made publicly available.
Feel free to explore, contribute, ask questions and provide feedback! 