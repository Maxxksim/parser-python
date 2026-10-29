from sqlalchemy.orm import mapped_column, Mapped, relationship

from models.answer import Answer
from models.answer_question import answer_question
from models.model import Model


class Question(Model):
    __tablename__ = 'questions'

    id: Mapped[int] = mapped_column(primary_key=True)
    question: Mapped[str] = mapped_column(unique=True)
    answer : Mapped[list[Answer]] = relationship(secondary=answer_question)