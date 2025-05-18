from sqlalchemy import (
    Column, Integer, Float, String, Enum,
    Date, Time, Boolean, ForeignKey
)
from sqlalchemy.orm import declarative_base, relationship
import enum

Base = declarative_base()

class WindDirectionEnum(enum.Enum):
    N = 'N'
    NNE = 'NNE'
    NE = 'NE'
    ENE = 'ENE'
    E = 'E'
    ESE = 'ESE'
    SE = 'SE'
    SSE = 'SSE'
    S = 'S'
    SSW = 'SSW'
    SW = 'SW'
    WSW = 'WSW'
    W = 'W'
    WNW = 'WNW'
    NW = 'NW'
    NNW = 'NNW'

class WindData(Base):
    __tablename__ = 'wind_data'

    id = Column(Integer, primary_key=True)
    weather_id = Column(Integer, ForeignKey('weather.id'), nullable=False)
    degree = Column(Integer, nullable=False)
    kph = Column(Float, nullable=False)
    direction = Column(Enum(WindDirectionEnum), nullable=False)
    go_out = Column(Boolean, nullable=False)

    weather = relationship("Weather", back_populates="wind")

class PrecipitationData(Base):
    __tablename__ = "precipitation_data"

    id = Column(Integer, primary_key=True)
    weather_id = Column(Integer, ForeignKey('weather.id'), nullable=False)
    pressure_mb = Column(Float, nullable=False)
    pressure_in = Column(Float, nullable=False)
    precip_mm = Column(Float, nullable=False)
    precip_in = Column(Float, nullable=False)
    humidity = Column(Integer, nullable=False)
    cloud = Column(Integer, nullable=False)

    weather = relationship("Weather", back_populates="precipitations")

class Weather(Base):
    __tablename__ = 'weather'

    id = Column(Integer, primary_key=True)
    country = Column(String(100), nullable=False)
    location_name = Column(String(100), nullable=False)
    last_updated = Column(Date, nullable=False)
    sunrise = Column(Time, nullable=False)

    wind = relationship("WindData", back_populates="weather", uselist=False)
    precipitations = relationship("PrecipitationData", back_populates="weather", uselist=False)

