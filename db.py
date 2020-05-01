from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

import os

db_inited = False
Base = declarative_base()


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    name = Column(String, default='')

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


def init_db():
    db_url = os.getenv("db_url")
    engine = create_engine(db_url)
    Base.metadata.create_all(bind=engine)
    global Session
    Session = sessionmaker(bind=engine)
    global db_inited
    db_inited = True


class TaskCondition(Base):
    __tablename__ = 'tasks_conditions'

    id = Column(Integer, primary_key=True)
    X = Column(ARRAY(Integer))
    B = Column(ARRAY(Integer))
    E = Column(ARRAY(Integer))

    task_id = Column(Integer, ForeignKey('tasks.id'))


def write_task_to_db(condition, answer, target_func_value, method=''):
    if not db_inited:
        init_db()
    B, E = [], []
    for i in condition:
        B.append(i[0])
        E.append(i[1])

    session = Session()
    task_condition = TaskCondition(B=B, E=E)
    solution = Solution(X=answer, metrics=target_func_value, method=method)
    task = Task(solutions=[solution], condition=task_condition)
    session.add(task)
    session.add(task_condition)
    session.add(solution)
    session.commit()
    session.close()

def show_db():
    if not db_inited:
        init_db()

    session = Session()
    tasks = [{'id': i.id, 'name': i.name} for i in session.query(Task).all()]
    conditions = [{'id': i.id, 'task_id': i.task_id, 'Experts E': i.E, 'Experts B': i.B}
                  for i in session.query(TaskCondition).all()]
    solutions = [{'id': i.id, 'task_id': i.task_id, 'Experts list': i.X, 'Metrics': i.metrics, 'Method': i.method}
                 for i in session.query(Solution).all()]

    return tasks, conditions, solutions

def get_presets_conditions():
    if not db_inited:
        init_db()
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
