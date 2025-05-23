try:
  import requests
except Exception as e:
  print(f"Error: {e}")

_url="http://ip-api.com/json/"

def Locate(_ip):
  _r = requests.get(_url+_ip).json()
  if _r["status"] == "success":
    print("Successfully Located :",_ip)
    print("Country: ", _r["country"])
    print("Region: ", _r["regionName"])
    print("City: ", _r["city"])
    print("ZIP: ", _r["zip"])
    print("Latitude: ", _r["lat"])
    print("Longitude: ", _r["lon"])
    print("Timezone: ", _r["timezone"])
    print("ISP: ", _r["isp"])
  else:
    print("Error! Please try again.")

def main():
  try:
    _ip = input("Enter an IP Address to Geolocate: ")
    Locate(_ip)
    input("Press enter to continue...")

  except Exception as e:
    print(f"Error: {e}")

if __name__ == "__main__":
  main()