import enum

from sqlalchemy import Column, Integer, String, Enum, DateTime
from api.database.init_db import Base

class SportType(enum.Enum):
    FOOTBALL = 'Football'
    BASKETBALL = 'Basketball'
    LEAGUE_OF_LEGENDS = 'League of Legends'
    CS_GO = 'CS:GO'
    BOXING = 'Boxing'
    MMA = 'MMA'

class GameStatus(enum.Enum):
    BEFORE = 'Before'
    PLAYING = 'Playing'
    FINISHED = 'Finished'

class Games(Base):
    __tablename__ = 'games'

    game_id = Column(Integer, primary_key=True)
    home = Column(String(100) , nullable=False)
    away = Column(String(100) , nullable=False)
    start_time = Column(DateTime , nullable=False)
    game_status = Column(Enum(GameStatus), nullable=False)
    sport_type = Column(Enum(SportType) , nullable=False)