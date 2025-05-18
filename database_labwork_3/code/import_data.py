import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Weather, WindData, PrecipitationData

# PostgreSQL
POSTGRES_URL = "postgresql://kyrylo:password@localhost:5432/lab3"
postgres_engine = create_engine(POSTGRES_URL)
PostgresSession = sessionmaker(bind = postgres_engine)
postgres_session = PostgresSession()

# MySQL
MYSQL_URL = "mysql+pymysql://kyrylo:password9@localhost:3306/lab3"
mysql_engine = create_engine(MYSQL_URL)
MySQLSession = sessionmaker(bind = mysql_engine)
mysql_session = MySQLSession()

# Create tables in both databases
Base.metadata.create_all(postgres_engine)
Base.metadata.create_all(mysql_engine)

def parse_time(t_str):
    from datetime import datetime
    return datetime.strptime(t_str, '%I:%M %p').time()

# Load CSV
file_path = r"C:\Users\user\Documents\database\database_labwork_3\code\GlobalWeatherRepository.csv"
df = pd.read_csv(file_path)

def insert_data(session):
    for _, r in df.iterrows():
        weather = Weather(
            country = r["country"],
            location_name = r["location_name"],
            last_updated = r["last_updated"],
            sunrise = parse_time(r["sunrise"])
        )
        session.add(weather)
        session.commit()

        wind = WindData(
            weather_id = weather.id,
            degree = r["wind_degree"],
            kph = r["wind_kph"],
            direction = r["wind_direction"],
            go_out = r["wind_kph"] <= 10
        )
        session.add(wind)

        precipitation = PrecipitationData(
            weather_id = weather.id,
            pressure_mb = float(r["pressure_mb"]),
            pressure_in = float(r["pressure_in"]),
            precip_mm = float(r["precip_mm"]),
            precip_in = float(r["precip_in"]),
            humidity = float(r["humidity"]),
            cloud = int(r["cloud"])
        )
        session.add(precipitation)

    session.commit()
    
# Insert into MySQL
insert_data(mysql_session)

# Insert into PostgreSQL
insert_data(postgres_session)