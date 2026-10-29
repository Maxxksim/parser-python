from sqlalchemy import Table, ForeignKey, Column
from models.model import Model

answer_question = Table(
    'answer_question',
    Model.metadata,
    Column('answer_id', ForeignKey('answers.id', ondelete='CASCADE'), primary_key=True),
    Column('question_id', ForeignKey('questions.id', ondelete='CASCADE'), primary_key=True),
)
