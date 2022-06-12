**EIA-DataPipeline** :: IN PROGRESS<br>
Creating a data pipeline to use the EIA's API and store into a local MySQL database for use in Power BI.

<br>

---

Directory

- [Project Overview](#project-overview)
- [Inital Research](#inital-research)
- [The Script](#the-script)
- [EIA API](#eia-api)

<br>

# Project Overview

This project is focused on creating my own MySQL database using data from the [Energy Information Administration](https://www.eia.gov/) via their API. The end goal is to have this data warehouse setup for SQL queries and to connect a Power BI Dashboard for visualizations and additional data exploration.

In addition to processing the data brought in from the EIA site, I want to take a shot at creating a local "data lake" and logs that will dump the raw JSON files into a folder and also create a log entry with file metadata to track when reports were run and other information.

<br>

**Tools**:

- Python
- MySQL Workbench
- SQL
- Power BI

**Packages** <br>
*For Python we will use the following packages, brief description here but I will explain the usage more as we move on.*

- pandas
- requests
- mysql.connector
- json

<br>

# Inital Research

- Looking to EIA site, understand their API and requirements.
- Difference between API v1 and API v2 and my difficulties

<br>

# The Script

- Bulding out the Python script, first steps and the outline/hopes 
- Debugging and creating more modular code
- see outline file for other things

<br>

# EIA API

- working with the API, things to look out for
- python packages required