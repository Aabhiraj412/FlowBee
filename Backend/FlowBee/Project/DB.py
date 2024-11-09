import os
from dotenv import load_dotenv
import pandas as pd
import mysql.connector
from mysql.connector import Error


def connectDB():
    # Step 1: Read the CSV file into a DataFrame
    df = pd.read_csv('./DATA/temp_data.csv')

    connection = None

    # Step 2: Connect to MySQL
    try:
        connection = mysql.connector.connect(
            host='localhost',  # Change to your MySQL host if different
            database='Flowbee',  # Replace with your database name
            user='root',  # Replace with your MySQL username
            password=os.getenv("MYSQL_PASS")  # Replace with your MySQL password
        )

        if connection and connection.is_connected():
            print("Successfully connected to MySQL")

            # Step 3: Prepare INSERT statement
            cursor = connection.cursor()
            
            # Adjust the table and column names as per your CSV and MySQL schema
            insert_query = """
                INSERT INTO DATA (reactions, comments, reposts, media_type, commentary_text) 
                VALUES (%s, %s, %s, %s, %s)
            """
            
            # Step 4: Insert data into MySQL
            for index, row in df.iterrows():
                data = (
                    row['reactions'],  # 'reactions' column in CSV
                    row['comments'],  # 'comments' column in CSV
                    row['reposts'],  # 'reposts' column in CSV
                    row['media_type'],  # 'media_type' column in CSV
                    row['commentary_text']  # 'commentary_text' column in CSV
                )
                cursor.execute(insert_query, data)
            
            # Commit the transaction
            connection.commit()
            print("Data successfully inserted into MySQL")
        
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
