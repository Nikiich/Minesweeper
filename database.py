from passlib.handlers.pbkdf2 import pbkdf2_sha256
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, text
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

engine = None
Session = None
Base = declarative_base()
initialized = False


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    username = Column(String, unique=True)
    password = Column(String)
    results = relationship('Result', back_populates='user')


class Result(Base):
    __tablename__ = 'results'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    score = Column(Integer)
    user = relationship('User', back_populates='results')


def initialize_database():
    global engine, Session
    engine = create_engine('sqlite:///users.db', echo=True)
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)


def create_user(username, password):
    session = Session()
    hashed_password = pbkdf2_sha256.hash(password)
    new_user = User(username=username, password=hashed_password)
    session.add(new_user)
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        print(str(e))
        session.close()
        return
    user = session.query(User).filter_by(username=username).first()
    session.close()
    return user


def if_exists_by_name(username):
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    session.close()
    if user is None:
        return False
    return True


def authenticate_user(username, password):
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    session.close()

    if user is None:
        return None
    res = pbkdf2_sha256.verify(password, user.password)
    if res:
        return user
    return None


def add_result(user_id, score):
    session = Session()
    user = session.query(User).get(user_id)

    if user is None:
        session.close()
        return False
    result = session.query(Result).get(user_id)
    if result is None:
        new_result = Result(user_id=user_id, score=score)
        session.add(new_result)
        session.commit()
        session.close()
        return True
    result.score = result.score + score
    session.commit()
    session.close()
    return True


def get_results(user_id):
    session = Session()
    user = session.query(User).get(user_id)

    if user is None:
        session.close()
        return None

    results = user.results
    session.close()
    return results


def get_all_results():
    global initialized
    if not initialized:
        initialize_database()
        initialized = True
    session = Session()
    query = text(
        "SELECT users.username as username, results.score AS score FROM results JOIN users ON results.user_id = users.id ORDER BY score DESC ")
    results = session.execute(query)
    session.close()
    formatted_results = []
    for res in results:
        formatted_result = f'{res.username} - {res.score}'
        formatted_results.append(formatted_result)
    return formatted_results
