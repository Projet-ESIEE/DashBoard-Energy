import requests

url = "https://www.example.com"

try:
    response = requests.get(url)
    response.raise_for_status()
    print("Internet access is available.")
except requests.exceptions.RequestException as e:
    print(f"Internet access is not available. Error: {e}")



from geopy.geocoders import Nominatim

def get_continent(country_name):
    geolocator = Nominatim(user_agent="continent_finder")
    location = geolocator.geocode(country_name, language='en')

    if location is not None:
        return location.raw.get('address', {}).get('continent', None)
    else:
        return None

# Example usage:
country_name = "United States"
continent = get_continent(country_name)

if continent:
    print(f"The continent of {country_name} is {continent}")
else:
    print(f"Continent information not found for {country_name}")