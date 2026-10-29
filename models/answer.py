from sqlalchemy.orm import mapped_column, Mapped, relationship
from models.answer_question import answer_question
from models.model import Model
from models.question import Question


class Answer(Model):
    __tablename__ = 'answers'

    id: Mapped[int] = mapped_column(primary_key=True)
    answer: Mapped[str] = mapped_column(unique=True)
    question: Mapped[list[Question]] = relationship(secondary=answer_question)