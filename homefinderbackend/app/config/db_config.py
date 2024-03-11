from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base  # Updated import path

# Base = declarative_base()
db_url = "postgresql://postgres:root@localhost:5432/homefinder_db"

Base = declarative_base()

engine = create_engine(db_url, echo=True)

SessionLocal = sessionmaker(bind=engine)
