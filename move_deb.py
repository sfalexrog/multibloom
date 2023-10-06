import os
import shutil


src_directory = os.path.abspath('./src')
destination_directory = os.path.join(os.path.dirname(src_directory), 'deb_files')


if not os.path.exists(destination_directory):
    os.makedirs(destination_directory)


for root, dirs, files in os.walk(src_directory):
    for file in files:
        if file.endswith('.deb'):
            src_file_path = os.path.join(root, file)
            dest_file_path = os.path.join(destination_directory, file)
            shutil.move(src_file_path, dest_file_path)

