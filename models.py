class Question:
    def __init__(self, id: str, text: str, quiz_id: str) -> None:
        self.id = id
        self.text = text
        self.quiz_id = quiz_id


class Option:
    def __init__(self, text: str, is_correct: bool, quiz_id: str, question_id: str) -> None:
        self.text = text
        self.is_correct = is_correct
        self.quiz_id = quiz_id
        self.question_id = question_id
