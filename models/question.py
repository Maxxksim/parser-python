from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship


from models.base_model import BaseModel

if TYPE_CHECKING:
    from models import Answer

class Question(BaseModel):
    __tablename__ = 'questions'

    id: Mapped[int] = mapped_column(primary_key=True)
    question: Mapped[str] = mapped_column(String(500), unique=True)
    answers: Mapped[list["Answer"]] = relationship(secondary="answer_question", back_populates="answers")
