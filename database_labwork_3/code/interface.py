from models import Base, Weather, WindData, PrecipitationData
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://kyrylo:157329@localhost:5432/lab3" 

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def get_valid_country(session):
    while True:
        country = input("Enter country: ").strip()
        exists = session.query(Weather).filter(Weather.country == country).first()
        if exists:
            return country
        print(f"No data found for country '{country}'. Please try again.")

def get_date_input():
    while True:
        date_str = input("Enter date (YYYY-MM-DD): ").strip()
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")

def fetch_weather_data(session, country, date):
    return session.query(Weather).join(WindData).filter(
        Weather.country == country,
        Weather.last_updated == date
    ).all()

def display_weather_info(weather, session):
    print(f"\n  Country: {weather.country}")
    print(f"  Last Updated: {weather.last_updated}")
    print(f"  Sunrise: {weather.sunrise}")

    wind_data = session.query(WindData).filter(WindData.weather_id == weather.id).all()
    for wind in wind_data:
        print(f"  Wind Direction: {wind.direction}")
        print(f"  Wind Speed (kph): {wind.kph}")
        print(f"  Wind Angle: {wind.degree}°")
        print(f"  Should Go Outside: {'Yes' if wind.go_out else 'No'}")

    precipitation_data = session.query(PrecipitationData).filter(
        PrecipitationData.weather_id == weather.id
    ).all()
    for p in precipitation_data:
        print(f"  Pressure (mb): {p.pressure_mb}")
        print(f"  Pressure (inches Hg): {p.pressure_in}")
        print(f"  Precipitation (mm): {p.precip_mm}")
        print(f"  Precipitation (inches): {p.precip_in}")
        print(f"  Humidity: {p.humidity}%")
        print(f"  Cloudiness: {p.cloud}%")

def interface():
    session = Session()
    try:
        country = get_valid_country(session)
        date = get_date_input()
        weather_data = fetch_weather_data(session, country, date)

        if not weather_data:
            print(f"No records found for country '{country}' on {date.date()}.")
            return

        for weather in weather_data:
            display_weather_info(weather, session)

    finally:
        session.close()

if __name__ == "__main__":
    interface()