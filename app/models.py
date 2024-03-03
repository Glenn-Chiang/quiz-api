import random
from typing import Optional
from app import db
from datetime import datetime, timezone
from sqlalchemy import String, ForeignKey, PrimaryKeyConstraint, ForeignKeyConstraint
from sqlalchemy.orm import mapped_column, Mapped, WriteOnlyMapped, relationship
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlite3 import Connection as SQLiteConnection
from flask import url_for
from werkzeug.security import generate_password_hash, check_password_hash


@event.listens_for(Engine, 'connect')
def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLiteConnection):
        cursor = dbapi_connection.cursor()
        cursor.execute('PRAGMA foreign_keys=ON')
        cursor.close()


class PaginatedMixin(object):
    @staticmethod
    def to_collection_dict(query, endpoint: str, page: int = 1, per_page: int = 20, **kwargs):
        pagination = db.paginate(query, page=page, per_page=per_page, error_out=False)

        return {
            'items': [item.to_dict() for item in pagination.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': pagination.pages,
                'total_items': pagination.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page, **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page, **kwargs) if pagination.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page, **kwargs) if pagination.has_prev else None
            }
        }


class User(PaginatedMixin, db.Model):
    __tablename__ = 'user_account' # Note that "user" is a reserved word in postgres, which is why we use another name here
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(25), unique=True, index=True)

    created_quizzes: WriteOnlyMapped['Quiz'] = relationship(
        'Quiz', back_populates='creator')
    quiz_attempts: WriteOnlyMapped['QuizAttempt'] = relationship(
        'QuizAttempt', back_populates='user')

    def __repr__(self) -> str:
        return f'User <{self.id}:{self.username}>'

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
        }

    def __init__(self, username: str, id: int = None) -> None:
        self.username = username
        if id:
            self.id = id

    # def set_password(self, password: str) -> None:
    #     self.password_hash = generate_password_hash(password)

    # def check_password(self, password: str) -> bool:
    #     return check_password_hash(pwhash=self.password_hash, password=password)


class Quiz(PaginatedMixin, db.Model):
    __tablename__ = 'quiz'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    subject: Mapped[str] = mapped_column(String(25))
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(tz=timezone.utc))

    # If the creator of a Quiz is deleted, the Quiz should remain
    creator_id: Mapped[int] = mapped_column(
        ForeignKey(User.id, ondelete='SET NULL'), index=True, nullable=True)
    creator: Mapped[User] = relationship(
        'User', back_populates='created_quizzes')

    # If a Quiz is deleted, all related Questions should be deleted
    questions = relationship(
        'Question', back_populates='quiz', passive_deletes=True, cascade='all, delete')

    # If a Quiz is deleted, related QuizAttempts should remain
    attempts: WriteOnlyMapped['QuizAttempt'] = relationship(
        'QuizAttempt', back_populates='quiz')

    def question_count(self):
        return len(self.questions)

    def __repr__(self) -> str:
        return f'Quiz <{self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'subject': self.subject,
            'created_at': self.created_at.isoformat(),
            'creator': self.creator.to_dict() if self.creator else None,
            'question_count': self.question_count()
        }

    def __init__(self, subject: str, creator_id: int | None = None) -> None:
        self.subject = subject
        self.creator_id = creator_id


class Question(PaginatedMixin, db.Model):
    __tablename__ = 'question'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(String(500))

    # If a Quiz is deleted, all related Questions should be deleted
    quiz_id: Mapped[int] = mapped_column(
        ForeignKey(Quiz.id, ondelete='CASCADE'), index=True)
    quiz: Mapped[Quiz] = relationship('Quiz', back_populates='questions')

    # If a Question is deleted, all related Choices should be deleted
    choices = relationship(
        'Choice', back_populates='question', passive_deletes=True, cascade='all,delete')

    attempted_questions: WriteOnlyMapped['AttemptQuestion'] = relationship(
        'AttemptQuestion', back_populates='question')

    def choices_count(self):
        return len(self.choices)

    def shuffle_choices(self):
        random.shuffle(self.choices)
        return self.choices

    def __repr__(self) -> str:
        return f'Question <{self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'quiz_id': self.quiz_id,
            'choices': [choice.to_dict() for choice in self.shuffle_choices()],
            'choices_count': self.choices_count()
        }

    def __init__(self, text: str, quiz_id: int) -> None:
        self.text = text
        self.quiz_id = quiz_id


class Choice(PaginatedMixin, db.Model):
    __tablename__ = 'choice'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(String(100))
    correct: Mapped[bool] = mapped_column()

    # If a Question is deleted, all related Choices should be deleted
    question_id: Mapped[int] = mapped_column(
        ForeignKey(Question.id, ondelete='CASCADE'), index=True)
    question: Mapped[Question] = relationship(
        'Question', back_populates='choices')

    user_choices: WriteOnlyMapped['UserChoice'] = relationship(
        'UserChoice', back_populates='choice')

    def __repr__(self) -> str:
        return f'Choice <{self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'correct': self.correct,
            'question_id': self.question_id
        }

    def __init__(self, text: str, correct: bool, question_id: int) -> None:
        self.text = text
        self.correct = correct
        self.question_id = question_id


class QuizAttempt(PaginatedMixin, db.Model):
    __tablename__ = 'quiz_attempt'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    timestamp: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(tz=timezone.utc), index=True)

    # If the Quiz associated with the QuizAttempt is deleted, set quiz_id to null and retain the QuizAttempt
    # This allows users to still view their QuizAttempts even if the related Quiz is deleted
    quiz_id: Mapped[int] = mapped_column(
        ForeignKey(Quiz.id, ondelete='SET NULL'), index=True, nullable=True)
    quiz: Mapped[Quiz] = relationship('Quiz', back_populates='attempts')

    # The User who made this QuizAttempt
    # If a User is deleted, their attempts should remain (?)
    user_id: Mapped[int] = mapped_column(ForeignKey(
        User.id, ondelete='SET NULL'), index=True, nullable=True)
    user: Mapped[User] = relationship('User', back_populates='quiz_attempts')

    # AttemptQuestions with sequence numbers
    questions = relationship('AttemptQuestion', back_populates='attempt',
                             passive_deletes=True, cascade='all, delete')

    user_choices: WriteOnlyMapped['UserChoice'] = relationship(
        'UserChoice', back_populates='attempt', passive_deletes=True, cascade='all, delete')

    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'quiz_id': self.quiz_id,
            'user_id': self.user_id,
            'attempted_questions': [question.to_dict() for question in self.questions]
        }

    def __init__(self, quiz_id: int, user_id: int) -> None:
        self.quiz_id = quiz_id
        self.user_id = user_id


# QuizAttempts contain Questions in a certain order that we want to retain.
# An AttemptQuestion stores the sequence_number of each Question in the Quiz to determine the order in which it appears in the QuizAttempt
class AttemptQuestion(PaginatedMixin, db.Model):
    __tablename__ = 'attempt_question'

    # attempt_id and question_id act as composite primary key
    attempt_id: Mapped[int] = mapped_column(ForeignKey(
        QuizAttempt.id, ondelete='CASCADE'), index=True, primary_key=True)
    attempt: Mapped[QuizAttempt] = relationship(
        'QuizAttempt', back_populates='questions')

    question_id: Mapped[int] = mapped_column(
        ForeignKey(Question.id, ondelete='SET NULL'), index=True, primary_key=True)
    question: Mapped[Question] = relationship(
        'Question', back_populates='attempted_questions')

    # To determine the order in which the Question appeared in the QuizAttempt
    sequence_number: Mapped[int] = mapped_column()

    def get_user_choice(self):
        user_choice = UserChoice.query.join(Choice, Choice.id == UserChoice.choice_id).filter(
            UserChoice.attempt_id == self.attempt_id, Choice.question_id == self.question_id).first()
        return user_choice.to_dict() if user_choice else None

    def to_dict(self):
        return {
            'attempt_id': self.attempt_id,
            'question_id': self.question_id,
            'question': self.question.to_dict(),
            'sequence_number': self.sequence_number,
            'user_choice': self.get_user_choice()
        }

    def __init__(self, attempt_id: int, question_id: int, sequence_number: int) -> None:
        self.attempt_id = attempt_id
        self.question_id = question_id
        self.sequence_number = sequence_number


# Choice chosen by User for an AttemptQuestion in a QuizAttempt
class UserChoice(PaginatedMixin, db.Model):
    __tablename__ = 'user_choice'

    # If choice is deleted (likely cascaded from deleting a Quiz), set choice_id to null
    choice_id: Mapped[int] = mapped_column(ForeignKey(
        Choice.id, ondelete='SET NULL'), primary_key=True, index=True, nullable=True)
    choice: Mapped[Choice] = relationship(
        'Choice', back_populates='user_choices')

    attempt_id: Mapped[int] = mapped_column(ForeignKey(
        QuizAttempt.id, ondelete='CASCADE'), primary_key=True, index=True)
    attempt: Mapped[QuizAttempt] = relationship(
        'QuizAttempt', back_populates='user_choices')

    def correct(self) -> bool:
        return self.choice.correct

    def to_dict(self):
        return {
            'id': self.id,
            'attempt_id': self.attempt_id,
            'user_id': self.attempt.user_id,
            'choice': self.choice.to_dict(),
            'correct': self.correct()
        }

    def __init__(self, attempt_id: int, choice_id: int) -> None:
        self.attempt_id = attempt_id
        self.choice_id = choice_id
