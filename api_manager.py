from amadeus import Client, ResponseError
from dotenv import load_dotenv
import os
import pandas as pd
import streamlit as st

load_dotenv()
class FlightAPI:
    def __init__(self):
        try:
            self.amadeus= Client(
                client_id=os.getenv("AMADEUS_API_KEY"),
                client_secret=os.getenv("AMADEUS_API_SECRET")
            )
            print("Api connected")
        except Exception as e:
            print(f"Not connected:{e}")

    def search_flights(self, origin, destination, departure_date):
        try:
            response = self.amadeus.shopping.flight_offers_search.get(
                originLocationCode=origin,
                destinationLocationCode=destination,
                departureDate=departure_date,
                adults=1,
                max=10
            )

            flights_data = []
            for flight in response.data:
                # 1. SETUP
                itinerary = flight['itineraries'][0]
                segments = itinerary['segments']
                airline_code = flight['validatingAirlineCodes'][0]

                # 2. CURRENCY CONVERSION LOGIC 💱
                # Get the raw price and currency from API (usually EUR)
                raw_price = float(flight['price']['total'])
                currency = flight['price']['currency']

                # Approximate conversion rates (Jan 2026 estimates)
                if currency == "EUR":
                    final_price = raw_price * 91.50  # 1 Euro = 91.5 INR
                elif currency == "USD":
                    final_price = raw_price * 84.00  # 1 USD = 84 INR
                else:
                    final_price = raw_price  # Fallback if unknown

                # 3. BUILD THE DATA
                offer = {
                    "Airline": airline_code,
                    "Flight_Num": f"{airline_code} {segments[0]['number']}",
                    "Source": origin,
                    "Destination": destination,
                    "Departure_Time": segments[0]['departure']['at'].replace("T", " "),
                    "Arrival_Time": segments[-1]['arrival']['at'].replace("T", " "),
                    "Duration": itinerary['duration'][2:],
                    "Stops": len(segments) - 1,

                    # Store converted price rounded to 2 decimal places
                    "Price": round(final_price, 2),
                    "Currency": "INR",  # Now hardcoded to INR

                    "Seats_Left": flight['numberOfBookableSeats'],
                    "Cabin": flight['travelerPricings'][0]['fareDetailsBySegment'][0]['cabin']
                }
                flights_data.append(offer)

            return pd.DataFrame(flights_data)

        except ResponseError as error:
            print(f"API Error: {error}")
            return pd.DataFrame()
        except Exception as e:
            print(f"General Error: {e}")
            return pd.DataFrame()