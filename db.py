from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

import os

db_url = os.getenv("db_url")

Base = declarative_base()


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    name = Column(String, default='Task #{}'.format(id))


class Solution(Base):
    __tablename__ = 'solutions'

    id = Column(Integer, primary_key=True)
    X = Column(ARRAY(Integer))
    metrics = Column(Integer)


class IntermediateResult(Base):
    __tablename__ = 'intermediate_result'

    id = Column(Integer, primary_key=True)
    X = Column(ARRAY(Integer))
    metrics = Column(Integer)


class TaskCondition(Base):
    __tablename__ = 'tasks_conditions'

    id = Column(Integer, primary_key=True)
    X = Column(ARRAY(Integer))
    B = Column(ARRAY(Integer))
    E = Column(ARRAY(Integer))


engine = create_engine(db_url)  # sqlite:///data/db/users.db
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)

session = Session()
u = Task(name='sdj312')
session.add(u)
session.commit()
print([(i.id, i.name) for i in session.query(Task).all()])

session.close()
