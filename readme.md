# yaml_generator.py

## Author:
  David Thomas - david_thomas@hakkoda.io

## Change Log:
  09/26/2022 - Created the .py file

## How to use this script

  - In your terminal runf the following command:
               
        python3 “path/to/schema-yml-generator.py” --csv_loc “path/to/src.csv”
  
  - The program expects a csv file with the following columns: 
    "Target Table", "Target Table Description", "Target Colum", "Target Column Description", "dbt test"

  - **Is advised to use the same csv format as the one obtained by downloading a Google sheets file as csv.** Check the example listed below for further details. 
  
  - To specify the path of the file use the following **_required_**  parameter:
           
        --csv_loc: Location of tha csv file to be processed. Wrap the path with "" if it contains any space on it. Ex: "a/b/c/.../path with space/"')

  - Using the optional parameter _--help_ will display the paramater details.

  - The output of the file is a dbt schema.yml file. It will be created in the same location of the csv file with the csv file name + the substring + _ _schema.yml_. 
  
    - Example: path/myfile.csv -> path/myfile_schema.yml

  - An example of an expected csv as input can be found [here](https://docs.google.com/spreadsheets/d/1UYNBYPsC4R_N_NTtaKFRfUk_4MsvdlRygyQDG9iMwwI/edit?usp=sharing).

  - An example of the expected .yml as output can be found [here](https://drive.google.com/file/d/14GaFrm3xW1yd7wIwExLFuwggIIeH7c-W/view?usp=sharing).

## Code summary
- What:
  - Python script that extracts table, column, tests, descriptions from csv into a dbt schema.yml compliant format.

- Why:
  - Automation of the dbt schema.yml creation. 
 
- How: 
  - The script captures the required information and builds a nested dictionary that stores the information. Then creates a yml file using the package ruamel.yaml
 
 
- Steps

      Step 0: Imports required modules & defines the .py parameters.
      Step 1: Function to read a csv file and obtain a dictionary for each row and stores them in a list.
      Step 2: Function to check if all the expected columns are present in the csv file specified by the user.
      Step 3: Function that runs over the list filled with dictionaries to capture the tables on the file, 
          creating a dictionary for each table.
      Step 4: Function in charge of creationg the dictionary of columns for each table.
      Step 5: Function that creates the yml file using the ruamel.yaml package.
      Step 6: Call to the mentioned functions and creation of the data structes the stores the information being processed.
 
## Dependencies:
- ruamel.yaml - https://yaml.readthedocs.io/en/latest/overview.html 
In order to instal it run the following commands:
    
    
    - pip install -U pip setuptools wheel
    - pip install ruamel.yaml
