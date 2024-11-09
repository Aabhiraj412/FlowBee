Source.py is the Starting Point of the Srcipt. It helps in collect profile information from such as Related Profiles and Post Data from given Profile.

Scrapper.py is a custom scripy made to extract necessary data from LinkedIn profiles

SaveCSV.py is custom scripy made to save all the data extracted from the profiles into given CSV file

DB.py is a custom scripy made to save all the data extracted from the profiles into the MySQL Database

All the extracted data from the profiles are also stored in a CSV file inside DATA folder

Steps to execute the script:

Step 1:
    Make sure that you are in Backend Directory

    cd Backend/FlowBee

Step 2:
    Make sure that all fileds in .env are correctly filled, i.e;
    
    LINKEDIN_USERNAME
    LINKEDIN_PASSWORD    
    MYSQL_PASS  (mysql Password)
    PROFILE_URL (LinkedIn Profile URL)

Step 3:
    Run the following command to execute the Python script

    poetry run python Project/Source.py

Step 4:
    Look for Extracted Data in DATA directory
    