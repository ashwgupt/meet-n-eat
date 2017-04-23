from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()


class userData(Base):
    __tablename__ = 'Users'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    password_hash = Column(String(250), nullable=False)
    email = Column(String(50), unique=True, nullable=False)


    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }


engine = create_engine('sqlite:///C:\\Users\\Admin\\development\\meet-n-eat\\generated\\Users.db')
Base.metadata.create_all(engine)