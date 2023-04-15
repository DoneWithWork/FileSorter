# Packages
import os
import shutil
from tqdm import tqdm
import datetime

# Default vars
now = datetime.datetime.now()
timer = now.strftime("%Y-%m-%d %H:%M:%S")
files_to_sort = False

print("Welcome to DoneWithWork's File Sorter")

# Get the folder location from the user

while True:
    folder_location = input("Enter the folder location: ")

    try:
        if len([f for f in os.listdir(folder_location) if os.path.isfile(os.path.join(folder_location, f))]) > 0:
            print("The folder contains files")
            files_to_sort = True
        if os.path.isdir(folder_location):
            print("Valid Directory")
            break
        else:
            print("Invalid directory, please try again.")
    except FileNotFoundError:
        print("Directory not found, please try again.")
if files_to_sort:
    # Ask the user if they want to sort subdirectories
    while True:
        subdirectories = input("Do you want to sort files in subdirectories? (y/n): ").lower()
        if subdirectories in ['y', 'n']:
            break
        else:
            print("Invalid input, please try again.")

    # Get the list of file extensions to exclude from sorting
    exclude_extensions = []
    while True:
        exclude_files = input("Do you want to exclude any file types? (y/n): ").lower()
        if exclude_files == 'n':
            break
        elif exclude_files == 'y':
            extensions = input("Enter the file extensions to exclude (separated by comma): ")
            exclude_extensions = [x.strip() for x in extensions.split(',')]
            exclude_extensions = [x.lower() for x in exclude_extensions if x != '']
            # Get the filename of the log file

            break
        else:
            print("Invalid input, please try again.")


    # Define a function to move files to the appropriate folders and log the movement
    def move_files(file, folder_location, folder_name, log_file):
        dest_folder = os.path.join(folder_location, folder_name)
        dest_file_path = os.path.join(dest_folder, file)
        if os.path.exists(dest_file_path):
            base_name, ext = os.path.splitext(file)
            i = 1
            while os.path.exists(os.path.join(dest_folder, f"{base_name}_{i}{ext}")):
                i += 1
            new_file_name = f"{base_name}_{i}{ext}"
            shutil.move(os.path.join(folder_location, file), os.path.join(dest_folder, new_file_name))
            log_file.write(f"Moved {file} to {os.path.join(dest_folder, new_file_name)}\n")
        else:
            shutil.move(os.path.join(folder_location, file), dest_file_path)
            log_file.write(f"Moved {file} to {dest_file_path}\n")


    # Initialize a counter variable to keep track of the number of files sorted
    file_count = 0

    log_filename = os.path.join(folder_location, "SortingFileLog.txt")
    with open(log_filename, 'w') as log_file:
        log_file.write("----  Sorting Files ----\n")
        log_file.write(f"Current time: {timer}\n")
        # Loop through all the files in the folder and sort them into appropriate folders
        for root, dirs, files in os.walk(folder_location):
            if not subdirectories == 'y':
                dirs.clear()  # if subdirectories == 'n', don't go into subdirectories
            for file in tqdm(files, desc="Sorting files", unit="file", total=len(files)):
                file_extension = os.path.splitext(file)[1][1:].lower()

                # Check if the file extension is in to exclude list
                if file_extension in exclude_extensions:
                    continue

                # Check if the current file being processed is the log file
                if file == "SortingFileLog.txt":
                    continue

                # Create a folder for the file extension if it doesn't exist
                folder_name = file_extension.upper()
                if not os.path.exists(os.path.join(folder_location, folder_name)):
                    os.makedirs(os.path.join(folder_location, folder_name))

                # Move the file to the appropriate folder and log the movement
                move_files(file, folder_location, folder_name, log_file)

                # Increment the file count
                file_count += 1

        # Print out the total number of files sorted
        print(f"{file_count} files sorted!")

        # Log the total number of files sorted
        log_file.write(f"\nTotal files sorted: {file_count}\n")

else:
    print("No Files to sort...")
while True:
    revert = input(
        "Do you want to revert all file movement and re-do? This also destroys any folders present as well. (y/n): ").lower()
    if revert == 'y':
        # Create a log file to track the reverted files
        log_file_path = os.path.join(folder_location, "SortingFileLog.txt")
        with open(log_file_path, "a") as log_file:
            log_file.write("---- Reverting File Sort ----\n")
            log_file.write(f"Current time: {timer}\n")
        # Loop through all the folders and move the files back to the original location
        for folder_name in os.listdir(folder_location):
            if os.path.isdir(os.path.join(folder_location, folder_name)):
                for file in os.listdir(os.path.join(folder_location, folder_name)):
                    shutil.move(os.path.join(folder_location, folder_name, file), os.path.join(folder_location, file))
                    # Log the reverted file
                    with open(log_file_path, "a") as log_file:
                        log_file.write(f"Reverted: {os.path.join(folder_name, file)}\n")
                os.rmdir(os.path.join(folder_location, folder_name))
                # Log the deleted folder
                with open(log_file_path, "a") as log_file:
                    log_file.write(f"Deleted folder: {os.path.join(folder_name)}\n")
        break
    elif revert == 'n':
        break
    else:
        print("Invalid input, please try again.")

# Print Statements
print("Done")
print("Feel Free to support me on my youtube and github, DoneWithWork :)")
