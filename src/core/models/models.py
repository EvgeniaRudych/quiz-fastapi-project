from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, true, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Quiz_result(Base):
    __tablename__ = "quiz_result"
    id = Column(Integer, primary_key=True, index=True)
    user_score = Column(Float, nullable=False)
    max_score = Column(Float, nullable=False)
    finished_at = Column(DateTime, default=datetime.now())
    user_id = Column(DateTime, default=datetime.now())


class Password(Base):
    __tablename__ = "password"

    id = Column(Integer, primary_key=True, index=True)
    password = Column(String, unique=True, index=True)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String, unique=True, index=True)
    is_superuser = Column(Boolean, default=False)
    password_id = relationship("Password", back_populates="password")
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())


class Categories(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String, index=True)


class Quizzes(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False)
    description = Column(String, index=True, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)


class Questions(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String, index=True, nullable=False)
    quiz_id = Column(ForeignKey("quizzes.id"))


class Answers(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    answer_text = Column(String, nullable=False)
    question_id = Column(ForeignKey("questions.id"))
    is_correct = Column(Boolean, nullable=False)


class Question_Categories(Base):
    __tablename__ = "question_categories"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(ForeignKey("questions.id"))
    category_id = Column(ForeignKey("categories.id"))
