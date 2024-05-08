
# Phonepe pulse Data Visualization

Extract data from the Phonepe pulse Github repository through scripting and
clone it.Transform the data into a suitable format and perform any necessary cleaning
and pre-processing steps. Insert the transformed data into a MySQL database for efficient storage and
retrieval.Create a live geo visualization dashboard using Streamlit and Plotly in Python
to display the data in an interactive and visually appealing manner. Fetch the data from the MySQL database to display in the dashboard.


## Tech Stack

**Client:** Python,Plotly,Pandas

**Server:** SQL,Streamlit


## Libraries
```
import pandas as pd
import mysql.connector as sql
import streamlit as st
import plotly.express as px
import os
import json
from streamlit_option_menu import option_menu
from PIL import Image
from git.repo.base import Repo
```

    
## Usage

To use this project, follow these steps:

1. Clone the repository
2. Install the required packages
3. Transform the data into a suitable format and  clean the data.
4. Insert the transformed data into a MySQL database for efficient storage 
5. Use plotly to visualize the data 
6. Run in Streamlit app  
## Approach

1. Data extraction: Clone the Github using scripting to fetch the data from the
Phonepe pulse Github repository and store it in a suitable format such as CSV
or JSON.

2. Data transformation: Use a scripting language such as Python, along with
libraries such as Pandas, to manipulate and pre-process the data. This may
include cleaning the data, handling missing values, and transforming the data
into a format suitable for analysis and visualization.

3. Database insertion: Use the "mysql-connector-python" library in Python to
connect to a MySQL database and insert the transformed data using SQL
commands.

4. Dashboard creation: Use the Streamlit and Plotly libraries in Python to create
an interactive and visually appealing dashboard. Plotly's built-in geo map
functions can be used to display the data on a map and Streamlit can be used
to create a user-friendly interface with multiple dropdown options for users to
select different facts and figures to display.

5. Data retrieval: Use the "mysql-connector-python" library to connect to the
MySQL database and fetch the data into a Pandas dataframe. Use the data in
the dataframe to update the dashboard dynamically.

6. Deployment: Ensure the solution is secure, efficient, and user-friendly. Test
the solution thoroughly and deploy the dashboard publicly, making it
accessible to users.

## Link

[Data link](https://github.com/PhonePe/pulse#readme) for getting Data from github clone




