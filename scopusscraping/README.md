# Data retrieval via the Scopus API

[![Project Status: Inactive – The project has reached a stable, usable state but is no longer being actively developed; support/maintenance will be provided as time allows.](https://www.repostatus.org/badges/latest/inactive.svg)](https://www.repostatus.org/#inactive)

The aim of this repository is to retrieve paper information from the [Scopus database](https://www.elsevier.com/en-gb/products/scopus), in an automated and efficient way, using their API. The query response can form a dataset to feed into the graph database made with [neo4j](https://gitlab.bham.ac.uk/missierp-ai4idai/neo4j).

## Accessing pre-run queries
 Thee queries use the full [list of University of Birmingham affiliations](data/uob_affils.csv). Also see this [scopus page](https://www.scopus.com/pages/organization/60019702#) for a summary of University of Birmingham Scopus documents.  

> The query responses are stored as json files on the Research Data Store (/rdsprojects/m/missierp-ai4idai/scopus_data). **If you are granted access to these and use them for your UoB research, it is assumed that you have read and agreed to the [API Service Agreement](https://dev.elsevier.com/policy/API-service-agreement.pdf), and also read Elsevier's policy on [Scopus API for academic research](https://dev.elsevier.com/academic_research_scopus.html).**

## Running your own queries

### Setting up your environment

Make a virtual python environment called 'venv_ai4idia' using the [requirements.txt](requirements.txt) file to install the required dependencies. Note, interaction with this code is presented as a Jupyter notebook, hence why there are many Jupyter-related dependencies listed in this requirements file. 

Installation example on a shell terminal:
- Create virtual Python environment: `python3 -m venv venv_ai4idia`
- Activate environment: `source venv_ai4idia/bin/activate`) 
- Install the required packages: `pip install -r requirements.txt` 

### Obtain Scopus API Key

- Go to [Elsevier Developer Portal](https://dev.elsevier.com) and select 'I want an API key'
- After signing in with UoB credentials, follow their instructions to create an API key 
- Copy the API Key from their website into an empty file called `.env` (this file should be kept private and therefore is not be tracked by git by including it in [.gitignore](.gitignore). See [.env.example](.env.example) to see what this file looks like).
- Note, for this key authentication to work you may have to be on campus (or using the UoB VPN)

### Interactive Coding Notebook

The [scopus_api.ipynb](code/scopus_api.ipynb) file was written and executed as [notebook file in Visual Studio Code](https://code.visualstudio.com/docs/datascience/jupyter-notebooks). If you want to run this coding notebook and create more query outputs from Scopus, you need to set up your environment with the necessary dependencies and authentications, as explained above.

For wider context, reference Scopus [general resources](https://dev.elsevier.com/documentation/SCOPUSSearchAPI.wadl), [search tips](https://dev.elsevier.com/sc_search_tips.html), [search views](https://dev.elsevier.com/sc_search_views.html) and [api_key settings](https://dev.elsevier.com/api_key_settings.html).



