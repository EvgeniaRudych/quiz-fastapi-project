import csv
import os
import pathlib
from datetime import datetime
from typing import List

import sqlalchemy
from fastapi import APIRouter, Depends
from fastapi import Request
from redis.client import Redis
from sqlalchemy import ForeignKey, and_, select, insert
from starlette import status

from connections import get_redis, get_database
from core.schemas.schemas import Quizzes, QuizzesInput, QuizWithQuestions, AnswerInput, QuizResult
from utils import get_user_info

router = APIRouter()

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


@router.get("/")
async def healthcheck(request: Request):
    return {"status": "Working"}


@router.get("/set/{key}/{value}/")
async def test(key: str, value: str, redis=Depends(get_redis)):
    redis.set(key, value)
    return redis.get(key)


@router.get("/api/v1/private/")
async def private(token: str = Depends(get_user_info)):
    return token


# QUIZZ CRUD
@router.get("/api/v1/quizzes/", response_model=List[Quizzes], status_code=200)
async def get_list_of_quizzes(database=Depends(get_database), token: str = Depends(get_user_info)):
    query = quizzes.select()
    list_of_quizzes = await database.fetch_all(query)
    return list_of_quizzes


@router.post("/api/v1/quizzes/", response_model=Quizzes, status_code=status.HTTP_201_CREATED)
async def create_quiz(database=Depends(get_database), quiz: QuizzesInput = Depends(),
                      token: str = Depends(get_user_info)):
    query = quizzes.insert().values(title=quiz.title, description=quiz.description, is_active=quiz.is_active).returning(
        quizzes.c.title, quizzes.c.description, quizzes.c.is_active)
    record_id = await database.execute(query)
    query = quizzes.select().where(quizzes.c.id == record_id)
    row = await database.fetch_one(query)
    return {**row}


# який джойн мені треба: квіз і усі питання які мають ФК на його айді, при цьому юзер авторизований, і також джойн питань та відповідей
# ми маємо також порахувати результат і записати його у поле юзера. Після цього hset

# мета: юзер натискає "пройти квіз" і бачить усі питання. /get/quizz/id/ підтягує квіз з його питаннями ЗРОБЛЕНО

# Потім відподає на питання і ми їх порівнюємо з відповідями, /post/quiz-res/id відправляє джейсон ({відповіді: питання}) користувача на сервер
# і там ми його порівнюємо з даними моделі answers і підраховуємо бали, потім записуємо їх у таблицю Quiz_result
# потім записуємо їх у редіс

@router.get("/api/v1/quizzes/{id}/", response_model=QuizWithQuestions, status_code=200)
async def get_quiz(id: int, database=Depends(get_database), token: str = Depends(get_user_info)):
    query = quizzes.select().where(quizzes.c.id == id)
    quiz = await database.fetch_one(query)
    quiz_questions_query = questions.select().where(questions.c.quiz_id == quiz.id)
    quiz_questions = await database.fetch_all(quiz_questions_query)
    return {"id": quiz.id, "title": quiz.title, "questions": quiz_questions}


# На цей ендпойнт юзер присилає відповіді {question: answer_text} - відповідей багато, тому це ліст.
# {
#   "questions": [{"q1":"answer1"}, {"q2":"answer2"}]
# }
# і там ми його порівнюємо з даними моделі answers і підраховуємо бали,
# потім записуємо їх у таблицю Quiz_result
# # потім записуємо їх у редіс
# далі треба зробити алгоритм порівняння відповідей юзера і відповідей що у моделі Answers
# вручну створюю змінну флоат, куда плюсую бали за кожну правильну відповідь
# цю зміну я записую у модель Quiz_result і її ж повертаю у респонсі

# {"azp": quiz_id, score}
# Редіс автоматично зберігає усі відповіді юзер на ОДИН квіз
# у вигляді {userid_quizid: {question1: "answer", quis2:answer} }
@router.post("/api/v1/pass/quizzes/{id}/", response_model=QuizResult, status_code=200)
async def pass_quizzes(id: int, answers_input: List[AnswerInput], database=Depends(get_database),
                       redis=Depends(get_redis),
                       token: str = Depends(get_user_info)):
    right_answers_query = select(answers.join(questions,
                                              and_(answers.c.question_id == questions.c.id, questions.c.quiz_id == id)))
    right_answers = await database.fetch_all(right_answers_query)
    quiz_score = 0
    dict_of_right_answers = {}
    for i in right_answers:
        dict_of_right_answers[i.question_id] = i.answer_text
    for i in answers_input:
        if i.answer_text == dict_of_right_answers[i.question_id]:
            quiz_score += 1
    query_insert_score = insert(quiz_result).values(user_score=quiz_score,
                                                    max_score=0, finished_at=datetime.now(), user_id=token.azp,
                                                    quiz_id=id)
    quiz_final_res = await database.execute(query_insert_score)
    get_user_results(token.azp, quiz_id=id, quiz_result_id=quiz_final_res, user_answers=answers_input,
                     redis_client=redis, quiz_score=quiz_score)
    return {"user_score": quiz_score}


# мій алгоритм csv: створюю файл і записую туди скор юзера.
# далі роблю перевірку у редісі чи існують результати користувача
# якщо вони існують, то теж записуємо їх у файл, усі файли зберігаємо у папку storage
# далі функція повертає файл.
# question_id, answer
def get_user_results(user_id, quiz_id, quiz_result_id, user_answers, redis_client: Redis, quiz_score):
    redis_key = f"{user_id}:{quiz_id}:{quiz_result_id}"
    res_to_save = {}
    for i in user_answers:
        res_to_save[i.question_id] = i.answer_text
    redis_client.hset(name=redis_key, mapping=res_to_save)
    with open(f"/home/evgenia/PycharmProjects/app/storage/{user_id}.csv", 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(["user_id","question&answer"])
        if redis_client.hgetall(name=redis_key) is not None:
            writer.writerow([user_id, redis_client.hgetall(name=redis_key)])
            return f


@router.patch("/api/v1/quizzes/{id}/", response_model=Quizzes, status_code=200)
async def update_quiz(id: int, database=Depends(get_database), quiz: Quizzes = Depends(),
                      token: str = Depends(get_user_info)):
    query = quizzes.insert().values(title=quiz.title, description=quiz.description, is_active=quiz.is_active)
    query = quizzes.select().where(quizzes.c.id == id)
    row = await database.fetch_one(query)
    return row


@router.delete("/api/v1/quizzes/{id}/", response_model=Quizzes)
async def delete_quiz(id: int, database=Depends(get_database), token: str = Depends(get_user_info)):
    query = quizzes.delete().where(quizzes.c.id == id)
    return await database.execute(query)


@router.get("/api/v1/results/", response_model=List[QuizResult], status_code=200)
async def see_results_of_all_users(database=Depends(get_database)):
    query = quiz_result.select()
    res_of_all_users = await database.fetch_all(query)
    return res_of_all_users


@router.get("/api/v1/results/{id}/", response_model=QuizResult, status_code=200)
async def see_results_of_user(id: int, database=Depends(get_database), token: str = Depends(get_user_info)):
    query = quiz_result.select().where(quiz_result.c.id == id)
    result = await database.fetch_one(query)
    return result
