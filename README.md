# PriceDropChecker

## About the Project

My PriceDropChecker project is a program written in Python. This program will take items saved by the user in a csv file, scrape prices on the e-Commerce website "Amazon", and notify the user through email about any found price-drops. 
(NOTE: to avoid a high volume of web-scraping, this project is only set up to check for price changes every 2 hours)

## Getting Started

#### Prerequisites
This program requires Python 3 to be run. Python3 can be downloaded here: https://www.python.org/downloads/

#### Installation
    git clone https://github.com/tsamonte/PriceDropChecker

#### Configuration File (config.yaml)
A skeleton [config.yaml](https://github.com/tsamonte/PriceDropChecker/blob/master/config.yaml) file is provided in this project. Before running, fill-in any required fields with relevant info. Optional fields do not need to be filled in, but if they are missing they may require additional user-input at runtime.

## Usage
This project runs directly on the command line. A makefile is provided for easy setup. To set-up a virtual environment, install all dependencies, and run the project, run the following command:

    make run

The above command will have the project run persistently and check for price drops every 2 hours. If running persistently is not preferred, this program can also be run just once using the following command:

    make run-once

#### Adding items to track
To track specific items from Amazon, all you need is to place the link in a specified csv file (file path should be specified in config.yaml). The csv file should be in the following format

|ID|Link|WebsiteName|ItemName|StartingPrice|PreviousLow|AllTimeLow|CurrentPrice
|---|---|---|---|---|---|---|---|
|1|https://www.amazon.com/dp/B0D1XD1ZV3||||||

A sample csv file with sample items is provided in [/data/sample-items.csv](https://github.com/tsamonte/PriceDropChecker/blob/master/data/sample-items.csv)
