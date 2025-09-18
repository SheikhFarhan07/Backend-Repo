from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        raise
    finally:
        db.close()