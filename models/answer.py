from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from models.base_model import BaseModel

if TYPE_CHECKING:
    from models import Question

class Answer(BaseModel):
    __tablename__ = 'answers'

    id: Mapped[int] = mapped_column(primary_key=True)
    answer: Mapped[str] = mapped_column(String(500), unique=True)
    questions: Mapped[list["Question"]] = relationship(secondary="answer_question", back_populates="answers")
