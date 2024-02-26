from typing import List
from app import db
from datetime import datetime, timezone
from sqlalchemy import String, ForeignKey, select, func
from sqlalchemy.orm import mapped_column, Mapped, WriteOnlyMapped, relationship


class User(db.Model):
    __tablename__ = 'user'
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

    def __init__(self, username: str) -> None:
        self.username = username


class Quiz(db.Model):
    __tablename__ = 'quiz'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    subject: Mapped[str] = mapped_column(String(25))
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(tz=timezone.utc))

    creator_id: Mapped[int] = mapped_column(ForeignKey(User.id), index=True)
    creator: Mapped[User] = relationship(
        'User', back_populates='created_quizzes')

    questions = relationship(
        'Question', back_populates='quiz')

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
            'creator': self.creator.to_dict(),
            'questions': [question.to_dict() for question in self.questions],
            'question_count': self.question_count()
        }

    def __init__(self, subject: str, creator_id: int) -> None:
        self.subject = subject
        self.creator_id = creator_id


class Question(db.Model):
    __tablename__ = 'question'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(String(100))

    quiz_id: Mapped[int] = mapped_column(ForeignKey(Quiz.id), index=True)
    quiz: Mapped[Quiz] = relationship('Quiz', back_populates='questions')

    choices = relationship(
        'Choice', back_populates='question')

    def choices_count(self):
        return len(self.choices)

    def __repr__(self) -> str:
        return f'Question <{self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'quiz_id': self.quiz_id,
            'choices': [choice.to_dict() for choice in self.choices],
            'choices-count': self.choices_count()
        }

    def __init__(self, text: str, quiz_id: int) -> None:
        self.text = text
        self.quiz_id = quiz_id

class Choice(db.Model):
    __tablename__ = 'choice'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(String(100))
    correct: Mapped[bool] = mapped_column()

    question_id: Mapped[int] = mapped_column(
        ForeignKey(Question.id), index=True)
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


class QuizAttempt(db.Model):
    __tablename__ = 'quiz_attempt'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    timestamp: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(tz=timezone.utc), index=True)

    quiz_id: Mapped[int] = mapped_column(ForeignKey(Quiz.id), index=True)
    quiz: Mapped[Quiz] = relationship('Quiz', back_populates='attempts')

    user_id: Mapped[int] = mapped_column(ForeignKey(User.id), index=True)
    user: Mapped[User] = relationship('User', back_populates='quiz_attempts')

    user_choices: WriteOnlyMapped['UserChoice'] = relationship(
        'UserChoice', back_populates='attempt')

    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'quiz_id': self.quiz_id,
            'user_id': self.user_id
        }

    def __init__(self, quiz_id: int, user_id: int) -> None:
        self.quiz_id = quiz_id
        self.user_id = user_id


class UserChoice(db.Model):
    __tablename__ = 'user_choice'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    attempt_id: Mapped[int] = mapped_column(
        ForeignKey(QuizAttempt.id), index=True)
    attempt: Mapped[QuizAttempt] = relationship(
        'QuizAttempt', back_populates='user_choices')

    choice_id: Mapped[int] = mapped_column(ForeignKey(Choice.id), index=True)
    choice: Mapped[Choice] = relationship(
        'Choice', back_populates='user_choices')

    def correct(self) -> bool:
        return self.choice.correct

    def to_dict(self):
        return {
            'id': self.id,
            'attempt_id': self.attempt_id,
            'choice': self.choice.to_dict(),
            'correct': self.correct()
        }

    def __init__(self, attempt_id: int, choice_id: int) -> None:
        self.attempt_id = attempt_id
        self.choice_id = choice_id
