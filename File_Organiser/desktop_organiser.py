import os
from pathlib import Path

listOfDirectories = {
  "Shortcuts": [".lnk"],
  "Zips": [".rar", ".zip", ".7z", ".rz", ".gz", ".iso", ".tar", ".dmz"],
  "PDFs": [".pdf"]
}

File_Format_Dictionary = {
  final_file_format: directory
  for directory, file_format_stored in listOfDirectories.items()
  for final_file_format in file_format_stored
}

def Organiser():
  try:
    os.mkdir("organiser")
  except Exception as e:
    print(f"Failed to create new directory: {e}")
  for entry in os.scandir():
    if entry.is_dir():
      continue
    file_path = Path(entry)
    if str(file_path) == "scripts.lnk":
      continue
    final_file_format = file_path.suffix.lower()
    if str(final_file_format) == ".code-workspace":
      continue
    if final_file_format in File_Format_Dictionary:
      directory_path = Path(File_Format_Dictionary[final_file_format])
      full_dir_path = Path("organiser/") / directory_path
      os.makedirs(full_dir_path, exist_ok=True)
      os.rename(file_path, full_dir_path / file_path.name)
      continue
    try:
      os.mkdir("organiser/Other")
    except Exception as e:
      print(f"Failed to create new directory: {e}")
    os.rename(file_path, os.getcwd() + "/organiser/Other/" + file_path.name)
    
    

def Change_Directory():
  _input = input("(p, l): ")
  if _input == "p":
    os.chdir(r"C:\\Users\D\Desktop")
  if _input == "l":
    os.chdir(r"C:\\Users\drodw\Desktop")
  else:
    print("Please input a correct character")
    Change_Directory()
  

def main():
  # asks user if is on desktop or laptop
  print("Hello Dylan, Are you on pc or laptop?")
  
  # changes directory conditionally if on pc or laptop
  Change_Directory()

  # organises files
  Organiser()
  
  input("Press enter to continue...")

if __name__ == "__main__":
  main()