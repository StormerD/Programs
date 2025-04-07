from Duplicate_Checker import duplicate_checker
from File_Organiser import desktop_organiser
from Ip_Geolocator import ip_locator
from Subnet_Calculator import subnet_calculator

programs_array = ["", "Duplicate Checker", "File Organiser", "IP Geolocator", "Subnet Calculator"]

def Logo_Bar():
  try:
    _logo = r"""
     _____  _                                       _____   
    / ____|| |                                     |  __ \  
   | (___  | |_  ___   _ __  _ __ ___    ___  _ __ | |  | | 
    \___ \ | __|/ _ \ | '__|| '_ ` _ \  / _ \| '__|| |  | | 
    ____) || |_| (_) || |   | | | | | ||  __/| |   | |__| | 
   |_____/  \__|\___/ |_|   |_| |_| |_| \___||_|   |_____/  
           _____              _         _                   
          / ____|            (_)       | |                  
         | (___    ___  _ __  _  _ __  | |_  ___            
          \___ \  / __|| '__|| || '_ \ | __|/ __|           
          ____) || (__ | |   | || |_) || |_ \__ \           
         |_____/  \___||_|   |_|| .__/  \__||___/           
                                | |                         
                                |_|                           
    """
  except Exception as e:
    print(f"Error: {e}")
    
  print(_logo)
  
def Print_Programs():
  i = 1
  while i < len(programs_array):
    print(f"[{str(i)}] {programs_array[i]}")
    i += 1
  print("[0] Exit")
    
def Program_Selector():
  _input = input("Select a program: ")
  print("- - - - - - - - - -")
  # exits program
  if _input == "0":
    exit()
  if _input == "1":
    duplicate_checker.main()
    main()
  if _input == "2":
    desktop_organiser.main()
    main()
  if _input == "3":
    ip_locator.main()
    main()
  if _input == "4":
    subnet_calculator.main()
    main()
  else:
    print("Please select a valid option...")
    Program_Selector()
  
def main():
  print("- - - - - - - - - -")
  Print_Programs()
  Program_Selector()
  
def init():
  try:
    
    Logo_Bar()
    main()
  except Exception as e:
    print(f"Error: {e}")
  
if __name__ == "__main__":
  init()