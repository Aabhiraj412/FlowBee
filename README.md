LinkedIn Scraping and Data Storage

Overview

    This project is a LinkedIn scraping tool that extracts profile data, including posts, reactions, comments, and reposts, from LinkedIn profiles. The tool uses Selenium with undetected-chromedriver for web scraping, stores the data in CSV files, and then uploads the data into a MySQL database for later use.

Features

    Login to LinkedIn: Logs into LinkedIn using your credentials.
    Profile Scraping: Scrapes LinkedIn profiles and their posts (including reactions, comments, reposts, and media types).

    Data Storage: Saves the scraped data into CSV files and stores it in a MySQL database.

    Redis Queue: Uses Redis to manage the queue of profile URLs to be processed.

    Parallel Scraping: Utilizes multithreading for parallel scraping of multiple profiles.

Setup Instructions

    Prerequisites:

        Python 3.x

    Make sure Python 3.x is installed on your system. You can check this by running:

        python --version

    MySQL Server

    Install and configure MySQL on your local machine or remote server. Create a database (e.g., Flowbee) and a table for storing scraped data:

        CREATE DATABASE Flowbee;

        USE Flowbee;

        CREATE TABLE DATA (
            id INT AUTO_INCREMENT PRIMARY KEY,
            profile_url VARCHAR(255),
            reactions INT,
            comments INT,
            reposts INT,
            media_type VARCHAR(50),
            commentary_text TEXT
        );

    Redis Server

    Install Redis and run it locally or on a server. You can install Redis from here.

Project Setup

    Poetry Installation

    If you don't have Poetry installed, you can install it by following the instructions from the official Poetry documentation.

    Install Dependencies

    After cloning or downloading the project, run the following command to install the required dependencies:

        poetry install

    Environment Configuration

    Create a .env file in the project root directory and add the following environment variables:

        LINKEDIN_USERNAME=your_linkedin_username
        LINKEDIN_PASSWORD=your_linkedin_password
        PROFILE_URL=starting_profile_url
        MYSQL_PASS=your_mysql_password

    Replace the placeholders with your actual LinkedIn credentials, MySQL password, and the URL of the first LinkedIn profile to scrape.

Usage

    Activate Poetry Virtual Environment

    Before running the project, activate the Poetry virtual environment:

        poetry shell

    Run the Scraper

    To start scraping, run the scraper.py file:

        python scraper.py
    
Functions

    Login: Logs into LinkedIn with the provided credentials.
    
    Profile Scraping: Scrapes the profile URL from the feed and retrieves posts, reactions, comments, reposts, and media.
    
    Data Storage: Appends data to CSV files (post_data.csv and temp_data.csv) and stores it in MySQL.
    
    Queue Management: Uses Redis to manage and process profile URLs for scraping.
    
File Breakdown

    Scraper.py
    
        Manages the scraping process, including login, profile scraping, and URL queuing using Redis.

    SaveCSV.py
        
        Handles saving scraped data into CSV files (post_data.csv and temp_data.csv) and clearing the temporary CSV file after data is stored in MySQL.

    DB.py
        
        Manages database connections and inserts data into MySQL after reading from the temp_data.csv file.

Troubleshooting

    CAPTCHA: If LinkedIn detects automated behavior, you may encounter a CAPTCHA. You'll need to manually solve it before the scraper can continue.

    Database Connection: Ensure MySQL is running and that your credentials in the .env file are correct.

    Redis Connection: Make sure Redis is running locally or on a server. Verify that the Redis host, port, and database are correct.

License

    This project is open-source and available under the MIT License.