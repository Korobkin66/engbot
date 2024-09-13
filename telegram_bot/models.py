from sqlalchemy.orm import (declarative_base, relationship,
                            sessionmaker)
from sqlalchemy import (Column, Integer, String, create_engine,
                        ForeignKey)

Base = declarative_base()

DATABASE_URL = "sqlite:///./telegram.db"
engine = create_engine(DATABASE_URL, echo=True)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String)
    channel = relationship("Channel", back_populates="owner")


class Channel(Base):
    __tablename__ = "channels"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    likn = Column(String)
    type = Column(String)
    owner = relationship("User", back_populates="channel")


Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
