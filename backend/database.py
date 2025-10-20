from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
import personal_config
'''
Create 'personal_config.py' in the project root directory and add the code (Change the password for your MySQL):
DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/event_everywhere?charset=utf8mb4"
'''

engine = create_engine(
    personal_config.DATABASE_URL,
    echo=True,
    pool_size=10,
    max_overflow=20,
    pool_recycle=280,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
