import os
from pathlib import Path


listOfDirectories = {
  "Shortcuts": [".lnk", ".exe", ".url"],
  "Zips": [".rar", ".zip", ".7z", ".rz", ".gz", ".iso", ".tar", ".dmz"],
  "PDFs": [".pdf"],
}


File_Format_Dictionary = {
  final_file_format: directory
  for directory, file_format_stored in listOfDirectories.items()
  for final_file_format in file_format_stored
}


def Organiser():
  duplicates = []
  try:
    os.makedirs("organiser", exist_ok=True)
    
  except Exception as e:
    print(f"Failed to create new directory: {e}")
    
  for entry in os.scandir():
    if entry.is_dir():
      continue
    
    file_path = Path(entry) # file on desktop
    
    if str(file_path) == "scripts.bat":
      continue
    
    final_file_format = file_path.suffix.lower() # desktop file format
    
    if str(final_file_format) == ".code-workspace":
      continue
    
    if final_file_format in File_Format_Dictionary:
      directory_path = Path(File_Format_Dictionary[final_file_format])
      full_dir_path = Path("organiser/") / directory_path
      os.makedirs(full_dir_path, exist_ok=True) # create directory if it doesn't exist
      dest_file_path = full_dir_path / file_path.name # destination file path
      
      if dest_file_path.exists():
        print(f"File already exists: {dest_file_path}")
        duplicates.append([file_path, dest_file_path]) # add duplicate file and dest path to list
        continue
      
      os.rename(file_path, dest_file_path)
      continue
    
    try:
      os.makedirs("organiser/Other", exist_ok=True)
      
    except Exception as e:
      print(f"Failed to create new directory: {e}")
      
    os.rename(file_path, os.getcwd() + "/organiser/Other/" + file_path.name)
  
  if duplicates:
    HandleDuplicates(duplicates)
  
    
def HandleDuplicates(duplicates):
  # message user for input
  print("Duplicates found:")
  print("Delete dup? Replace to dest? Choose for each one? Skip all?")
  _input = input("Please select (D, R, C, S): ")
  # Handle user input
  if _input.lower() == "d": # delete duplicates
    for dup, dest in duplicates:
      try:
        dup.unlink() # delete duplicate file
        print(f"Deleted duplicate file: {dup}")
      except Exception as e:
        print(f"Failed to delete duplicate file: {e}")
        
  elif _input.lower() == "r": # replace duplicates in destination
    for dup, dest in duplicates:
      try:
        dest.unlink() # delete destination file
        print(f"Deleted destination file: {dest}")
        os.rename(dup, dest) # move duplicate to destination
        print(f"Moved duplicate file to destination: {dest}")
      except Exception as e:
        print(f"Failed to move duplicate file to destination: {e}")
        
  elif _input.lower() == "c": # choose for each duplicate
    for dup, dest in duplicates:
      print(f"Duplicate file: {dup}")
      print("Delete? Replace to dest? Skip?")
      _cInput = input("Please select (D, R, S): ")
      if _cInput.lower() == "d": # delete duplicate
        try:
          dup.unlink() # delete duplicate file
          print(f"Deleted duplicate file: {dup}")
        except Exception as e:
          print(f"Failed to delete duplicate file: {e}")
          
      elif _cInput.lower() == "r": # replace duplicate in destination
        try:
          dest.unlink() # delete destination file
          print(f"Deleted destination file: {dest}")
          os.rename(dup, dest) # move duplicate to destination
          print(f"Moved duplicate file to destination: {dest}")
        except Exception as e:
          print(f"Failed to move duplicate file to destination: {e}")
          
      elif _cInput.lower() == "s": # skip duplicate
        print(f"Skipped duplicate file: {dup}")
        
      else: # invalid input
        print("Please input a correct character")
        HandleDuplicates(duplicates)
  
  elif _input.lower() == "s": # skip all duplicates
    print("Skipped all duplicates")
    
  else: # invalid input
    print("Please input a correct character")
    HandleDuplicates(duplicates)
  

def Change_Directory():
  _input = input("(P, L): ")
  if _input.lower() == "p":
    os.chdir(r"C:\\Users\D\Desktop")
  elif _input.lower() == "l":
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