class TriviaQuestion():
    question: list | str
    correct_answer: str
    incorrect_answer_1: str
    incorrect_answer_2: str
    incorrect_answer_3: str
    author: str

    def __init__(self, 
                 question: list[str] | str, 
                 author: str,
                 topic_name: str,
                 correct_answer: str, 
                 incorrect_answer_1: str, 
                 incorrect_answer_2: str, 
                 incorrect_answer_3: str | None = None,
                 ) -> None:
        self.author = author
        self.game = topic_name
        self.question = question
        self.correct_answer = correct_answer
        self.incorrect_answer_1 = incorrect_answer_1
        self.incorrect_answer_2 = incorrect_answer_2
        if incorrect_answer_3 is None:
            self.incorrect_answer_3 = "None are correct :)"
        else:
            self.incorrect_answer_3 = incorrect_answer_3
    
    def fetch_incorrect_answers(self) -> list[str]:
        return [self.incorrect_answer_1, self.incorrect_answer_2, self.incorrect_answer_3]


class Topic():
    topic_name: str
    easy_questions: list[TriviaQuestion]
    medium_questions: list[TriviaQuestion]
    hard_questions: list[TriviaQuestion]

    def __init__(self, 
                 topic_name: str, 
                 easy_questions: list[TriviaQuestion], 
                 medium_questions: list[TriviaQuestion], 
                 hard_questions: list[TriviaQuestion]
                 ) -> None:
        self.topic_name = topic_name
        self.easy_questions = easy_questions.copy()
        self.medium_questions = medium_questions.copy()
        self.hard_questions = hard_questions.copy()

    def fetch_every_question(self) -> list[TriviaQuestion]:
        return self.easy_questions + self.medium_questions + self.hard_questions

