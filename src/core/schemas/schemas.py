import typing
from pydantic import BaseModel


class UserInfoToken(BaseModel):
    iss: str
    sub: str
    aud: str
    iat: int
    exp: int
    azp: str
    gty: str


class Quizzes(BaseModel):
    id: int
    title: str
    description: str
    is_active: bool


class QuizzesInput(BaseModel):
    title: str
    description: str
    is_active: bool


class Answers(BaseModel):
    id: int
    answer_text: str
    question_id: int
    is_correct: bool


class AnswerInput(BaseModel):
    question_id: int
    answer_text: str


class Questions(BaseModel):
    id: int
    question_text: str
    quiz_id: int


class QuizWithQuestions(BaseModel):
    id: int
    questions: typing.List[Questions]


class QuizResult(BaseModel):
    user_score: float


class QuestionsInput(BaseModel):
    question_text: str


class Categories(BaseModel):
    id: int
    name: str
    description: str


class QuestionCategories(BaseModel):
    id: int
    question_id: int
    category_id: int
