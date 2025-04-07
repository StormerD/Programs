from File_Organiser import desktop_organiser
from IP_Geolocator import ip_locator
from Subnet_Calculator import subnet_calculator

programs_array = ["", "File Organiser", "IP Geolocator", "Subnet Calculator", "Duplicate Checker"]

def Logo_Bar():
  _logo = """
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
    desktop_organiser.main()
    main()
  if _input == "2":
    subnet_calculator.main()
    main()
  
def init():
  Logo_Bar()
  main()
  
def main():
  print("- - - - - - - - - -")
  Print_Programs()
  Program_Selector()
  
if __name__ == "__main__":
  init()