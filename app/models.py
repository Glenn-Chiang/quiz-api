from app import db
from datetime import datetime, timezone
from sqlalchemy import String, ForeignKey
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
        return f'User <{self.username}>'
    

class Quiz(db.Model):
    __tablename__ = 'quiz'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    subject: Mapped[str] = mapped_column(String(25))
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(tz=timezone.utc))

    creator_id: Mapped[int] = mapped_column(ForeignKey(User.id), index=True)
    creator: Mapped[User] = relationship(
        'User', back_populates='created_quizzes')

    questions: WriteOnlyMapped['Question'] = relationship(
        'Question', back_populates='quiz')

    attempts: WriteOnlyMapped['QuizAttempt'] = relationship(
        'QuizAttempt', back_populates='quiz')

    def __repr__(self) -> str:
        return f'Quiz <{self.id}>'

class Question(db.Model):
    __tablename__ = 'question'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(String(100))

    quiz_id: Mapped[int] = mapped_column(ForeignKey(Quiz.id), index=True)
    quiz: Mapped[Quiz] = relationship('Quiz', back_populates='questions')

    choices: WriteOnlyMapped['Choice'] = relationship(
        'Choice', back_populates='question')

    def __repr__(self) -> str:
        return f'Question <{self.id}>'

class Choice(db.Model):
    __tablename__ = 'choice'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(String(100))
    is_correct: Mapped[bool]

    question_id: Mapped[int] = mapped_column(
        ForeignKey(Question.id), index=True)
    question: Mapped[Question] = relationship(
        'Question', back_populates='choices')

    user_choices: WriteOnlyMapped['UserChoice'] = relationship(
        'UserChoice', back_populates='choice')

    def __repr__(self) -> str:
        return f'Choice <{self.id}>'

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
