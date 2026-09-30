from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./fitbuddy.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    user_id = Column(String, unique=True, nullable=False)
    age = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    goal = Column(String, nullable=False)
    intensity = Column(String, nullable=False)
    original_plan = Column(Text)
    updated_plan = Column(Text)
    feedback = Column(Text)


Base.metadata.create_all(bind=engine)


def get_original_plan(user_id: str):
    db = SessionLocal()

    user = db.query(User).filter(User.user_id == user_id).first()

    db.close()

    if user:
        return user.original_plan

    return None


def update_plan(user_id: str, updated_plan: str, feedback: str):
    db = SessionLocal()

    user = db.query(User).filter(User.user_id == user_id).first()

    if user:
        user.updated_plan = updated_plan
        user.feedback = feedback
        db.commit()

    db.close()