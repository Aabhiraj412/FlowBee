import csv
import time
import os
from DB import connectDB

def append_data(Data):
    csv_filename = "./DATA/post_data.csv"
    with open(csv_filename, mode="a", newline="", encoding="utf-8") as csv_file:
        fieldnames = ['reactions', 'comments', 'reposts', 'media_type', 'commentary_text']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Check if the file is empty before writing header
        if csv_file.tell() == 0:
            writer.writeheader()  # Write the header only if the file is empty

        writer.writerows(Data)  # Write each post's data as a row

    print(f"Data appended to {csv_filename}")
    # time.sleep(3)  # Wait before returning to the main loop
    # os.system('clear')


def temp_data(Data):
    csv_filename = "./DATA/temp_data.csv"
    with open(csv_filename, mode="a", newline="", encoding="utf-8") as csv_file:
        fieldnames = ['reactions', 'comments', 'reposts', 'media_type', 'commentary_text']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Check if the file is empty before writing header
        if csv_file.tell() == 0:
            writer.writeheader()  # Write the header only if the file is empty

        writer.writerows(Data)  # Write each post's data as a row

    print(f"Data appended to {csv_filename}")

    # Storing data in database
    connectDB()

    # Clear the CSV file after storing data in the database
    os.remove(csv_filename)
    # Open the CSV file in write mode ('w')
    # csv', 'w', newline='') as file:
    #     pass  # Do nothing, just open the file in write mode to clear its contents

    time.sleep(3)  # Wait before returning to the main loop
    os.system('clear')