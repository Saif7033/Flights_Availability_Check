# city_data.py
airports = {
    "New Delhi": "DEL",
    "Mumbai": "BOM",
    "Bangalore": "BLR",
    "Chennai": "MAA",
    "Kolkata": "CCU",
    "Hyderabad": "HYD",
    "Dubai": "DXB",
    "London (Heathrow)": "LHR",
    "New York (JFK)": "JFK",
    "Singapore": "SIN"
}

def get_city_names():
    return list(airports.keys())

def get_airport_code(city_name):
    return airports.get(city_name)