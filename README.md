**EIA-DataPipeline** :: IN PROGRESS<br>
Creating a data pipeline to use the EIA's API and store into a local MySQL data warehouse for use in Power BI.

---

Directory

- [Project Overview](#project-overview)
- [Initial Research](#initial-research)
- [EIA API](#eia-api)
- [Creating the Data Warehouse](#creating-the-data-warehouse)
- [The Script](#the-script)
- [Power BI](#power-bi)
- [Conclusion](#conclusion)

<br>

# Project Overview

This project is focused on creating my own MySQL data warehouse using data from the [Energy Information Administration](https://www.eia.gov/) via their API. The end goal is to have this data warehouse setup for SQL queries and to connect a Power BI Dashboard for visualizations and additional data exploration.

In addition to processing the data brought in from the EIA site, I want to take a shot at creating a local "data lake" and logs that will dump the raw JSON files into a folder and also create a log entry with file metadata to track when reports were run and other information.

I will likely continue to work this project as I bring in additional information I find over time and improve the insights that can be extracted from the various data points.

**Tools**:

- Python
- MySQL Workbench
- SQL
- Power BI

**Packages**: <br>

- pandas
- requests
- mysql.connector
- json

**Current Data Sources**:

- CO2 Emissions by State
- Coal Consumption by State

I will first go over the major steps in this project, going over each of the tools used and any issues that I had along with how I resolved them. After these sections I will go into the analysis and observations I had gleamed from the information.

<br>

# Initial Research

The source for our data for this project comes from the [EIA](https://www.eia.gov/) website and there is a large amount of information available for download either through Excel files or their API. The general idea for this pipeline and analysis is to get data on emissions and energy usage by various states to see what patterns exist and what questions may come up from such data.

The EIA currently has two API's setup, their older v1 API and their new v2 API which have different processes for getting information. Originally I was not aware of the new v2 API and setup my python script to work with the v1 tooling. Additionally, when I attempted to work with the v2 API the documentation was not quite clear as to how to get exactly the reporting you are looking for. For these reason I continued with the v1 API so keep this in mind if you are working with the v2 you will have to change your code.

I also looked into which data warehouse server I wanted to use for this project, and historically I have already used MSSQL Server and PostgreSQL for other personal projects so I wanted to try out MySQL for this one. For the backend visualizations and dashboard I originally wanted to work with Tableau but after looking into the public version of the software it is not possible to install the MySQL connector to directly plug into the server. Instead we will be using Power BI which enables a large amount of connection options.

<br>

# EIA API

Working with the EIA v1 API is quite simple, for each report set you want to download there will be a URL constructed that points to the specific report (such as coal usage by month by state). With this in mind I knew I would need a secondary datasource which had U.S. State names and their abbreviations in order to build the URL for every state available. 

General API usage applies here, you will be working with JSON, converting them into python dictionaries or pandas DataFrames to clean and transform the data prior to insertion into the data warehouse. In order to do this within python you will need to work with a few packages, below is the package name you will pip/conda install if you do not have it:

- APIs through `requests`
- MySQL connection through `sql-connector-python`
- Data manipulation through `pandas`
- Work with JSON from the API through `json`

AN alternative here is to use a package called `sqlalchemy` to work with databases, I'm not sure if there are any additional requirements to use that package but that is something to take a look at.


<br>

# Creating the Data Warehouse

Creating the MySQL data tables is supper straightforward thankfully through the use of the [MySQL Community Installer](https://dev.mysql.com/downloads/mysql/), just make sure to install:

- MySQL Server
- MySQL Workbench
- Connector for Python
- Connector for NET

If you are using PowerBI with MySQL you will need the Connector for NET mentioned above, but there was an issue that came up when I attempted to connect to the database. This issue comes up because there is a missing line in the config file for the connector when you download the most recent version, to resolve this issue:

- Make sure you download the up to date version of the Connector for .NET
- Go to the following path/file location 
            
        *C:\Windows\Microsoft.NET\Framework64\v4.0.30319\Config\machine.config* 
            
- In this config file you will need to CTRL + F (Find) and search the text "DbProviderFactories", there is a subsection that looks like there is something missing between two lines of the same text, looks like this

        <DbProviderFactories>
        <DbProviderFactories>

- In between these tags copy and past the following line to reference the new version of the connector

        <add name="MySQL Data Provider" invariant="MySql.Data.MySqlClient" description=".Net Framework Data Provider for MySQL" type="MySql.Data.MySqlClient.MySqlClientFactory, MySql.Data, Version=8.0.29.0, Culture=neutral, PublicKeyToken=c5687fc88969c44d" />

I wanted to bring this up now in the event that the same issue comes up for you while using Power BI + MySQL. For the table setup you can check out the SQL file I have save in the `code` folder within this repo.

<br>

# The Script

- Bulding out the Python script, first steps and the outline/hopes 
- Debugging and creating more modular code
- see outline file for other things

For the script(s) we need to make sure we are planning for a few key components: API, data transformation, and database connection. EAch unit of this process has its own set of subprocesses, I want to break this down conceptually because there are likely many other way to execute these steps.

**API Calls**

- Pull in API key information from config file
- Setup the URL(s) that will be called, loop over this list
- Process JSON response
- Store meta date regarding the API call

**Data Transformations**

- Bring in the JSON resopnse into `pandas` dataframe
- Diagnostic checks: data types, NULL's, column names, calculations, etc.
  
**Database Connection**

- Establish database connectivity 
- For each API call, execute SQL query to load data into appropriate tables
- At the end of the script, close connection


<br>

# Power BI

As mentioned previously, there were some issues connection Power BI to the MySQL database that I had setup. The core of the problem came from the installed connector on the MySQL side which allowed Power BI to use the proper protocols.

After this issue was resolved, I was able to properly see all my tables and begin setting up a temp dashboard to ensure that the information is what I am looking for and testing out some layouts.

![Sample Power BI Visuals](images\sample_powerBI_visuals_01.PNG)

The goal here is to take a look at some comparisons between states that are close to each other on the West coast and identify any trends. 

<br>

# Conclusion

This project was a great exercise in working with an API to get data for further processing and later visualization. I think that looking back the biggest update that could be done would be to the gerneral scripts structure as there are similar functions called in order to process the URL's and make the GET requests as well as inserting into the database. There is likely a better OOP approach to reduce the redundancy in code and making the setup more extensible.

As for expanding this project, it would be great to bring in information from other sources outside of EIA and look at ways of combining the data and generating more insightful analysis. I would look to bring in U.S. car sales or information similar to this in order to compare emissions and energy usage in comparison to gas car sales and EV car sales.