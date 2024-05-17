# File System Baseline and Output to CSV
# Josh Jobe
# 1 May 2024
# Ver. 1.1
# Minor revisions to handles errors

#When the script is executed, it will ask for a directory to scan and a directory to save
#the file csv file.  This is best to run on a freshly built system to have a baseline
#to compare to in the future if you suspect changes were made.  The results of the scan
#will be saved to a CSV file with the File Path, Filename, and SHA256 hash for each file.

#Example on a Windows System (using VS Code):
#C:\ScriptFolder> & "C:/Program Files/Python311/python.exe" c:/ScriptFolder/system_baseline.py
#Enter the root directory to scan: C:\Users\username\Documents\
#Enter the output CSV file path (including filename): C:\Users\username\Documents\document_folder_baseline.csv
#Scan completed. CSV file created and renamed to: C:\Users\username\Documents\document_folder_baseline_8e2bf9cb.csv

#Example on Ubuntu:
#$ python system_baseline.py 
#Enter the root directory to scan: /home/user/Documents
#Enter the output CSV file path (including filename): /home/user/Documents/documents_folder_baseline.csv
#Scan completed. CSV file created and renamed to: /home/user/Documents/documents_folder_baseline_28a51db8.csv



import os
import hashlib
import csv

def calculate_sha256(file_path):
    """Calculate SHA256 hash of a file."""
    sha256 = hashlib.sha256()
    try:
       with open(file_path, 'rb') as f:
           while True:
               data = f.read(65536)  # Read in chunks of 64KB
               if not data:
                   break
               sha256.update(data)
    except FileNotFoundError:
        # Skip the file if it's not found
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        # Handle other exceptions if needed
        print(f"Error processing file {file_path}: {e}")
        return None
    return sha256.hexdigest()

def scan_system(root_dir):
    """Scan the system starting from the root directory."""
    files_info = []
    for folder, _, filenames in os.walk(root_dir):
        for filename in filenames:
            file_path = os.path.join(folder, filename)
            sha256_hash = calculate_sha256(file_path)
            files_info.append((file_path, filename, sha256_hash))
    return files_info

def write_to_csv(files_info, output_file):
    """Write files information to a CSV file."""
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(output_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['File Path', 'Filename', 'SHA256 Hash'])
        csv_writer.writerows(files_info)

def rename_csv_with_hash(output_csv_file):
    """Rename the CSV file with its SHA256 hash."""
    csv_hash = calculate_sha256(output_csv_file)
    new_filename = f"{output_csv_file[:-4]}_{csv_hash[:8]}.csv"
    os.rename(output_csv_file, new_filename)
    return new_filename

if __name__ == "__main__":
    root_directory = input("Enter the root directory to scan: ")
    output_csv_file = input("Enter the output CSV file path (including filename): ")

    files_info = scan_system(root_directory)
    write_to_csv(files_info, output_csv_file)

    renamed_csv_file = rename_csv_with_hash(output_csv_file)
    print(f"Scan completed. CSV file created and renamed to: {renamed_csv_file}")
