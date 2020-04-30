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

    solutions = relationship("Solution")  # one to many
    intermediate_results = relationship("IntermediateResult")  # one to many
    condition = relationship("TaskCondition", backref='task', uselist=False)  # one to one


class Solution(Base):
    __tablename__ = 'solutions'

    id = Column(Integer, primary_key=True)
    X = Column(ARRAY(Integer))
    metrics = Column(Integer)
    method = Column(String)

    task_id = Column(Integer, ForeignKey('tasks.id'))


class IntermediateResult(Base):
    __tablename__ = 'intermediate_results'

    id = Column(Integer, primary_key=True)
    X = Column(ARRAY(Integer))
    metrics = Column(Integer)

    task_id = Column(Integer, ForeignKey('tasks.id'))


class TaskCondition(Base):
    __tablename__ = 'tasks_conditions'

    id = Column(Integer, primary_key=True)
    X = Column(ARRAY(Integer))
    B = Column(ARRAY(Integer))
    E = Column(ARRAY(Integer))

    task_id = Column(Integer, ForeignKey('tasks.id'))


engine = create_engine(db_url)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)


def get_presets_conditions():
    session = Session()
    all_tasks = session.query(Task).all()
    conditions_ids = [task.condition.id for task in all_tasks]
    conditions = session.query(TaskCondition).filter(TaskCondition.id.in_(conditions_ids)).all()

    presets = []
    for condition in conditions:
        be = []
        for b, e in zip(condition.B, condition.E):
            be.append((b, e))

        presets.append({
            'task_id': condition.task_id,
            'experts': be
        })

    session.close()
    return presets

# u = Task(name='sdj312')
# session.add(u)
# session.commit()
# print([(i.id, i.name) for i in session.query(Task).all()])
#

