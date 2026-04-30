from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///emails.db")
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class EmailLog(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True)
    subject = Column(String)
    category = Column(String)
    response = Column(Text)

Base.metadata.create_all(engine)