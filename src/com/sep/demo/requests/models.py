from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()


class requestData(Base):
    __tablename__ = 'Request'

    user_id = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    meal_type = Column(String(250), nullable=False)
    latitude = Column(String(250), nullable=False)
    longitude = Column(String(250), nullable=False)
    location_string = Column(String(250), nullable=False)
    meal_time = Column(String(50), nullable=False)
    filled = Column(Boolean, default=False)


    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'user_id': self.user_id,
            'id': self.id,
            'meal_type': self.meal_type,
            'location_string': self.location_string,
            'meal_time': self.meal_time,
            'filled': self.filled
        }


engine = create_engine('sqlite:///../../../../generated/Request.db')
Base.metadata.create_all(engine)