# Questions.py
#
# TODO: Add class description here
#
# Author[s]:
#   Monish Gupta
#   Paul C Carlson
# Class: CS 5340 - Fall 2018
# Date: 24 October 2018
#


class Questions:
    def __init__(self, question_path, question_id):
        self.question_file_name = "{}{}.questions".format(question_path, question_id)
        self.qset_id = question_id
        self.questions = []
        # Read in all of the questions from the question file
        self.__retrieve_questions()

    # Returns the question file in it's original form
    def __repr__(self):
        all_questions = ""
        for q in self.questions:
            all_questions = "{}{}\n".format(all_questions, q)
        return all_questions

    #
    def __retrieve_questions(self):
        with open(self.question_file_name) as qf:
            qid = ""
            qstr = ""
            qdiff = ""
            for line in qf:
                if line.startswith("QuestionID:"):
                    qid = " ".join(line.strip('\n').split(' ')[1:])
                elif line.startswith("Question:"):
                    qstr = " ".join(line.strip('\n').split(' ')[1:])
                elif line.startswith("Difficulty:"):
                    qdiff = " ".join(line.strip('\n').split(' ')[1:])
                    self.questions.append(Question(qid, qstr, qdiff))


#
class Question:
    def __init__(self, qid, question, difficulty):
        self.qid = qid
        self.question = question
        self.difficulty = difficulty

        self.type = ""

        self.words = []
        self.__split_into_words()

    # Returns the question in its original form
    def __repr__(self):
        return "QuestionID: {}\nQuestion: {}\nDifficulty: {}\n".format(
            self.qid, self.question, self.difficulty
        )

    # Really simple way to type the questions - doesn't seem to capture much
    # meaning
    def __split_into_words(self):
        q = self.question.replace('?', '')
        self.words = q.split(' ')
        for w in self.words:
            w.strip()
        if 'who' in (w.lower() for w in self.words):
            self.type = 'WHO'
        elif 'what' in (w.lower() for w in self.words):
            self.type = 'WHAT'
        elif 'when' in (w.lower() for w in self.words):
            self.type = 'WHEN'
        elif 'where' in (w.lower() for w in self.words):
            self.type = 'WHERE'
        elif 'why' in (w.lower() for w in self.words):
            self.type = 'WHY'
        elif 'whose' in (w.lower() for w in self.words):
            self.type = 'WHOSE'
        elif ('how' and 'many') in (w.lower() for w in self.words):
            self.type = 'HOW MANY'
        elif 'how' in (w.lower() for w in self.words):
            self.type = 'HOW'

