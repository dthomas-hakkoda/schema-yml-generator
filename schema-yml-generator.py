#!/usr/bin/env python
# coding: utf-8

"""
-- yaml_generator.py
--
-- Author:
--  David Thomas - david_thomas@hakkoda.io
--
-- Change Log:
--  09/26/2022 - Created the .py file
--
-- What:
--  Python script that extracts table, column, tests, descriptions from csv into a dbt schema.yml compliant format.
-- Why:
--  Automation of the dbt schema.yml creation. 
-- How:
--  The script captures the required information and builds a nested dictionary that stores the information. Then creates a 
--  yml file using the package ruamel.yaml
-- 
-- Steps
--      Step 0: Imports required modules & defines the .py parameters.
--      Step 1: Function to read a csv file and obtain a dictionary for each row and stores them in a list.
--      Step 2: Function to check if all the expected columns are present in the csv file specified by the user.
--      Step 3: Function that runs over the list filled with dictionaries to capture the tables on the file, 
--          creating a dictionary for each table.
--      Step 4: Function in charge of creationg the dictionary of columns for each table.
--      Step 5: Function that creates the yml file using the ruamel.yaml package.
--      Step 6: Call to the mentioned functions and creation of the data structes the stores the information being processed.
-- 
-- Dependencies:
--  ruamel.yaml - https://yaml.readthedocs.io/en/latest/overview.html 
--  In order to instal it run the following commands:
--      pip install -U pip setuptools wheel
--      pip install ruamel.yaml

"""


############################################################################
################################### Step 0 #################################
############################################################################

'''
-- What:
--  Imports required packages and define how to parse command line arguments.
-- Why:
--  In order to use the packages and receive  command line arguments.
-- How:
--  Implementing imports and establish how to parse command line arguments through the argparse package.
'''

import csv
import re
import argparse
import os
from ruamel.yaml import YAML


# through argparse package, the .py parses command line arguments
# additionaly includes the .py file description and help options for each argument

parser = argparse.ArgumentParser(
    description='YAML generator using a csv file as source with the following columns: '+
        'Target Table, Target Table Description, Target Column, Target Column Description, dbt test')
parser.add_argument('--csv_loc', type=str, required=True,
                    help='Location of tha csv file to be processed. Wrap the path with "" if it contains any space on it. Ex: "a/b/c/.../path with space/"')
args = parser.parse_args()
csvLoc = args.csv_loc

############################################################################
################################### Step 1 #################################
############################################################################

'''
-- What:
--  Function that reads a csv file and obtain a dictionary for each row and stores them in a list.
-- Why:
--  Capture all the information in the csv file. 
-- How:
--  Creates a dictionary for each row and store each dictionary in a list.
'''


def csv_to_dict (csv_location):

    try:
        list_of_dict =[*csv.DictReader(open(csv_location))]

        return (list_of_dict)
    
    except:
        print('\nUnable to read specified csv\n\n' + csv_location + '\n')
        print('End of the program\n')
        quit()




############################################################################
################################### Step 2 #################################
############################################################################

'''
-- What:
--  Function to check if all the expected columns are present in the csv file specified by the user.
-- Why:
--  Avoid exceptions during the processing of the file due to not recognized keys.
-- How:
--  Test if all the expected columns are present in the list of columns of the first dictionary on the list.
--  Terminates the program if not all the expected columns are found.
'''
def columns_check():

    list_keys= list(list_of_dict[0].keys())

    expected_keys = ["Target Table", "Target Table Description", "Target Column Description", "dbt test"] 
        
    check = all(item in list_keys for item in expected_keys)

    if check is False:
        print('\nThe specified csv does not have the expected columns, please modify it accordingly\n\n')
        for c in expected_keys:
            print(c)        

        print('\n\nEnd of the program\n')
        quit()

############################################################################
################################### Step 3 #################################
############################################################################

'''
-- What:
--  Function that runs over the list filled with dictionaries to capture the tables on the file, 
--    creating a dictionary for each table.
--  Additionaly, defines the version of the file, required for dbt.
-- Why:
--  The YAML package uses nested dictionaries to handle the information. Hence, this step defines the table keys. 
-- How:
--  Iterates over the list of dictionaries capturing the tables details in a dictionary. Then, append it to the models list.
'''

def init_dictionary():

    dictionary['version'] = 2

    dictionary['models'] = []

    for d in list_of_dict:

        if ( d["Target Table"] and d["Target Column"]) :
            table_dict = {}
            table_dict["name"]= d["Target Table"]
            table_dict["description"]= d["Target Table Description"]

            table_dict["columns"]= []
            
            if table_dict not in dictionary['models']:
                    dictionary['models'].append(table_dict)

############################################################################
################################### Step 4 #################################
############################################################################

'''
-- What:
--  Function in charge of creationg the dictionary of columns for each table.
-- Why:
--  The YAML package uses nested dictionaries to handle the information. Hence, this step add the columns details for each table found. 
-- How:
--  Iterates over the list of dictionaries capturing the column details in a dictionary and append it to the columns list of each table.
'''

def fill_columns():       
    for d in list_of_dict:
        if ( d["Target Table"]> "" and d["Target Column"] > "") :
        
            if d["Target Column"]> "":
                column_dict = {}
                column_dict["name"]= d["Target Column"]

                if d["Target Column Description"]> "":
                    column_dict["description"]= d["Target Column Description"]

                if d["dbt test"] > "":

                    test_list = (re.findall('\w+', d["dbt test"]))

                    column_dict["tests"]= test_list
                
                for i in (dictionary['models']):
                    if i['name'] == d["Target Table"]:
                        i['columns'].append(column_dict)

############################################################################
################################### Step 5 #################################
############################################################################

'''
-- What:
--  Function that creates the yml file using the ruamel.yaml package.
-- Why:
--  To obtain final .yml file.
-- How:
--  Captures the original path and replaces the format of the file to add the substring "_schema.yml"
--  Then, writes the YAML into the yml file through the dump operation using a specified format.
'''

def file_writer():

    size = len(csvLoc)
    replacement = '_schema.yml'
    file_name = csvLoc.replace(csvLoc[size - 4:], replacement)

    with open(file_name, 'w') as fp:
        yaml = YAML()
        yaml.indent(mapping=5, sequence=3, offset=1)
        yaml.dump(dictionary, fp)

    print('\nThe following file was created successfully: \n\n' + file_name + '\n')    
    print('End of the program\n')

############################################################################
################################### Step 6 #################################
############################################################################


'''
-- What:
--  Call to the mentioned functions and creation of the data structes the stores the informatio being processed.
-- Why:
--  To run all the described process.
-- How:
--  Defining the objects to be used and then running the functions.
'''

dictionary = {}

list_of_dict = csv_to_dict(csvLoc)
columns_check()
init_dictionary()
fill_columns()
file_writer()