**EIA-DataPipeline** :: IN PROGRESS<br>
Creating a data pipeline to use the EIA's API and store into a local MySQL data warehouse for use in Power BI.

<br>

---

Directory

- [Project Overview](#project-overview)
- [Initial Research](#initial-research)
- [EIA API](#eia-api)
- [Creating the Data Warehouse](#creating-the-data-warehouse)
- [The Script](#the-script)
- [Power BI](#power-bi)
- [Analysis and Thoughts](#analysis-and-thoughts)
- [Conclusion](#conclusion)

<br>

# Project Overview

This project is focused on creating my own MySQL data warehouse using data from the [Energy Information Administration](https://www.eia.gov/) via their API. The end goal is to have this data warehouse setup for SQL queries and to connect a Power BI Dashboard for visualizations and additional data exploration.

In addition to processing the data brought in from the EIA site, I want to take a shot at creating a local "data lake" and logs that will dump the raw JSON files into a folder and also create a log entry with file metadata to track when reports were run and other information.

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
  - *C:\Windows\Microsoft.NET\Framework64\v4.0.30319\Config\machine.config* 
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

<br>

# Power BI

- connecting to mysql, all those issues
- setting up the data model (creating date table, confirming data types)


<br>

# Analysis and Thoughts

- go over the EDA process and some of the visualizations in the darboard
- interesting things that I saw and some questions I'd have for further research


<br>

# Conclusion

