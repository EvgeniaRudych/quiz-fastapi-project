import sqlalchemy
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

metadata = sqlalchemy.MetaData()

quizzes = sqlalchemy.Table(
    "quizzes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String(500)),
    sqlalchemy.Column("description", sqlalchemy.String(500)),
    sqlalchemy.Column("is_active", sqlalchemy.Boolean)

)

questions = sqlalchemy.Table(
    "questions",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("quiz_id", sqlalchemy.Integer, ForeignKey("quizzes.id")),
    sqlalchemy.Column("question_text", sqlalchemy.String(500))

)

answers = sqlalchemy.Table(
    "answers",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("answer_text", sqlalchemy.String),
    sqlalchemy.Column("question_id", sqlalchemy.Integer, ForeignKey("questions.id")),

)

categories = sqlalchemy.Table(
    "categories",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("question_text", sqlalchemy.String(500)),
    sqlalchemy.Column("description", sqlalchemy.String(500))

)

question_categories = sqlalchemy.Table(
    "question_categories",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("question_id", sqlalchemy.Integer, ForeignKey("questions.id")),
    sqlalchemy.Column("category_id", sqlalchemy.Integer, ForeignKey("categories.id"))

)

quiz_result = sqlalchemy.Table(
    "quiz_result",
    metadata,

    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_score", sqlalchemy.Float),
    sqlalchemy.Column("max_score", sqlalchemy.Float),
    sqlalchemy.Column("finished_at", sqlalchemy.DateTime),
    sqlalchemy.Column("user_id", sqlalchemy.String),
    sqlalchemy.Column("quiz_id", sqlalchemy.Integer, ForeignKey("quizzes.id"))

)
