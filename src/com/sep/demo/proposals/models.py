from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()


class proposalData(Base):
    __tablename__ = 'Proposal'

    request_id = Column(Integer, nullable=False)
    id = Column(Integer, primary_key=True)
    user_proposed_to = Column(String(250), nullable=False)
    user_proposed_from = Column(String(250), nullable=False)
    filled = Column(Boolean, default=False)


    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'request_id': self.request_id,
            'id': self.id,
            'user_proposed_to': self.user_proposed_to,
            'user_proposed_from': self.user_proposed_from,
            'filled': self.filled
        }


engine = create_engine('sqlite:///proposals/Proposal.db')
Base.metadata.create_all(engine)