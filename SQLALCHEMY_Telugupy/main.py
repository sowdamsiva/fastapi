from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer,String
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "postgresql://postgres:root@localhost:5432/postgres"

engine  = create_engine(DATABASE_URL,echo = False)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

Base = declarative_base()

class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)

    def __repr__(self):
        return f"id={self.id}, name = {self.name}, age={self.age}"

Base.metadata.create_all(engine)

#create
# user1 = User(name="ram",age=29)
# user2 = User(name="krish", age=27)

# session.add_all([user1,user2])
# session.commit()

#read all users
users = session.query(User).all()
print(users)

#read single user

# single = session.query(User).filter_by(name="siva").first()
# print(single)
# print(single.name,single.age)

#conditinal user
# users = session.query(User).filter(User.age>27).all()
# print(users)

#update
# ram = session.query(User).filter_by(name="ram").first()
# ram.age=35
# session.commit()

#delete
# ram = session.query(User).filter_by(name="ram").first()
# session.delete(ram)
# session.commit()