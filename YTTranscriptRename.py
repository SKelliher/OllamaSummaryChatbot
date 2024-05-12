import os
import shutil

# Set the directory path and the block of text to insert
directory_path = 'C:/Users/St\x20John/MyDocuments/Library/LBR_Process'
insert_text = '---' + '\n'
insert_text +=  'tags: ' + '\n'
insert_text +=  ' - transcript' + '\n'
insert_text +=  'URL: ' + '\n'
insert_text +=  'Author: ' + '\n'
insert_text +=  'Title: ' + '\n'
insert_text +=  'Published: ' + '\n'
insert_text +=  'Seconds: ' + '\n'
insert_text +=  '---' + '\n'

# Loop through all files in the directory
for filename in os.listdir(directory_path):
    # Check if the file has a .txt extension
    if filename.endswith('.txt'):
        # Open the file and read its contents
        file_path = os.path.join(directory_path, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            file_contents = file.read()

        # Insert the block of text at the beginning of the file contents
        new_contents = insert_text + file_contents

        # Create a new file with the same name but with a .md extension
        new_filename = filename.replace('.txt', '.md')
        new_file_path = os.path.join(directory_path, new_filename)

        # Write the new contents to the new file
        with open(new_file_path, 'w', encoding='utf-8') as new_file:
            new_file.write(new_contents)

        # Remove the original file
        os.remove(file_path)