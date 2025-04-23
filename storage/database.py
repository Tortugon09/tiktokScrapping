import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

Base = declarative_base()

class Video(Base):
    __tablename__ = 'videos'
    id = Column(String(255), primary_key=True)
    description = Column(Text)
    likes = Column(Integer)
    author = Column(String(255))
    playCount = Column(Integer)
    comments = Column(Integer)
    video_url = Column(String(500))
    comments_list = Column(JSON)

# Conexión a MySQL usando variables de entorno
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_DB = os.getenv("MYSQL_DB")

DATABASE_URL = (
    f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
)

engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)

def save_videos(video_list):
    session = Session()
    for v in video_list:
        session.merge(Video(**v))
    session.commit()
    session.close()
