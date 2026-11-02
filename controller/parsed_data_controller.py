import json

from sqlalchemy import select, insert

from database.db import Db
from models import Question, Answer, answer_question


class ParsedDataController:
    def __init__(self, db: Db):
        self._db = db

    def save_data(self, data: str):
        converted_data = json.loads(data)

        for questions in converted_data.values():

            for question_text, answers_with_lengths in questions.items():
                question = self._db.connection.scalar(
                    select(Question).where(Question.question == question_text)
                )

                if question is None:
                    question = Question(question=question_text)
                    self._db.connection.add(question)

                self._db.connection.execute(insert(Answer).prefix_with("IGNORE"), answers_with_lengths)

                only_answers = []

                for answer_with_length in answers_with_lengths:
                    only_answers.append(answer_with_length["answer"])

                answers_ids = self._db.connection.scalars(
                    select(Answer.id).where(Answer.answer.in_(only_answers))
                ).all()

                question_answers_ids = []

                for answer_id in answers_ids:
                    question_answers_ids.append({
                        'question_id': question.id,
                        'answer_id': answer_id,
                    })

                self._db.connection.execute(insert(answer_question), question_answers_ids).prefix_with("IGNORE")

        self._db.connection.commit()

        return next(iter(converted_data))
