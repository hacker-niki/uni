import os


def search_files(directory, extension):
  for root, directories, files in os.walk(directory):
      for file in files:
        if file.endswith(extension):
          file_path = os.path.abspath(os.path.join(root, file))
          print(file_path)

