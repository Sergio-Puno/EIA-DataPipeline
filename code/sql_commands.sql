-- FIRST TABLE INFO --
-- Create database to store our coal consumption data
CREATE DATABASE coal_consumption;

-- We have to explicitly select our new database for use, otherwise new tables will go elsewhere
USE coal_consumption;

-- View tables in a database
SHOW TABLES;

-- Create our table for coal consumption records
CREATE TABLE state_consumption (
	report_date DATETIME,
    coal_consumption DOUBLE,
    state VARCHAR(2)
);

-- Confirm that the table was create and is in the structure we specified
SHOW TABLES;
DESCRIBE state_consumption;

-- While testing the script for multiple file entries, I need this script to reset the database from scratch
DROP TABLE state_consumption;

CREATE TABLE state_consumption (
	report_date DATETIME,
    coal_consumption DOUBLE,
    state VARCHAR(2)
);

DESCRIBE state_consumption;

-- Checking my import worked with a simple aggregation
SELECT
    state
    , SUM(coal_consumption) as total_consumption
FROM state_consumption
GROUP BY state
ORDER BY total_consumption DESC;


-- SECOND TABLE INFO --
-- Working on the second table of co2 emission information
CREATE TABLE co2_emissions (
	period DATETIME,
    series_name VARCHAR(30),
    sector_name VARCHAR(30),
    fuel_name VARCHAR(30),
    state_id VARCHAR(2),
    state_name VARCHAR(30)
);