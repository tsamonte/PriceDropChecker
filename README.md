# PriceDropChecker

## About the Project

My PriceDropChecker project is a program written in Python. This program will take items saved by the user in a csv file, scrape prices on the e-Commerce website "Amazon", and notify the user through email about any found price-drops. 
(NOTE: to avoid a high volume of web-scraping, this project is only set up to check for price changes every 2 hours)

## Getting Started

#### Prerequisites
This program requires Python 3 to be run. Python3 can be downloaded here: https://www.python.org/downloads/

#### Installation
    git clone https://github.com/tsamonte/PriceDropChecker

## Usage
This project runs directly on the command line. A makefile is provided for easy setup. To set-up a virtual environment, install all dependencies, and run the project, run the following command:

    make run

The above command will have the project run persistently and check for price drops every 2 hours. If running persistently is not preferred, this program can also be run just once using the following command:

    make run-once
