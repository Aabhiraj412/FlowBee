import csv


def append_data(Data):
    csv_filename = "post_data.csv"
    with open(csv_filename, mode="a", newline="", encoding="utf-8") as csv_file:
        fieldnames = ["reactions", "comments", "reposts","commentary_text"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Check if the file is empty before writing header
        if csv_file.tell() == 0:
            writer.writeheader()  # Write the header only if the file is empty

        writer.writerows(Data)  # Write each post's data as a row

    print(f"Data appended to {csv_filename}")