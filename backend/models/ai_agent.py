from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class AIAgent(Base):
    __tablename__ = 'ai_agents'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    specialty = Column(String(100))

    def __repr__(self):
        return f"<AIAgent(id={self.id}, name='{self.name}', specialty='{self.specialty}')>"