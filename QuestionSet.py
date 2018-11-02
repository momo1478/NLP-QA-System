# QuestionSet.py
#
# TODO: Add class description here
#
# Author[s]:
#   Monish Gupta
#   Paul C Carlson
# Class: CS 5340 - Fall 2018
# Date: 24 October 2018
#


class QuestionSet:
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

    # Get the parts of each question from the designated file
    # questions are of the form:
    # QuestionID: <qid>
    # Question: <qstr>
    # Dificullty: <qdiff>
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


# TODO: Add a class description?
class Question:
    # This seems like a silly approach really ...
    measure_words = ['many', 'much', 'often', 'big', 'small', 'few', 'tall', 'short', 'heavy', 'light',
                     'fast', 'slow', 'old', 'new', 'far', 'near', 'close']
    question_words = ['who', 'whom', 'whose', 'what', 'when', 'where', 'why', 'how']

    def __init__(self, qid, question, difficulty):
        self.qid = qid
        self.qstr = question
        self.words = []
        self.difficulty = difficulty

        # Main question type
        self.type = "NONE"
        # Question word that occurs later in a sentence, assumed to be a supporting question word
        self.support_type = "NONE"
        # Part of sentence that precedes the first question word, assumed to condition the question
        self.conditional = "NONE"

        self.__split_into_words()
        self.__determine_question_type()

    # Returns the question in its original form
    def __repr__(self):
        return "QuestionID: {}\nQuestion: {}\nDifficulty: {}\n".format(
            self.qid, self.qstr, self.difficulty
        )

    # split the question into an array of words and remove the '?'
    def __split_into_words(self):
        q = self.qstr.replace('?' , '').replace(',' , '')
        self.words = str(x for x in q.split(' '))
        for w in self.words:
            w.strip()

    # Simple implementation for determining question type, just check for 'WH' words
    # Doesn't really seem to capture much meaning
    # TODO: Come up with rules to determine the important things to look for in answers
    def __determine_question_type(self):
        type_pos = len(self.qstr)
        q = self.qstr.lower()

        # TODO: Use WordNet to pull this information instead, the attribute of the word
        # directly following how ... e.g.
        # many - numerousness -> count
        # big - size -> number ... ?
        for m in self.measure_words:
            mstr = "how {}".format(m)
            if mstr in self.qstr.lower():
                pos = self.qstr.lower().find(mstr)
                if pos < type_pos:
                    type_pos = pos
                    self.type = 'MEASURE'
                    self.support_type = m.upper()
                else:
                    self.support_type = 'MEASURE'

        if 'who' in q or 'whom' in q or 'whose' in q:
            pos = q.index('who')
            if pos < type_pos:
                type_pos = pos
                self.type = 'WHO'
            else:
                self.support_type = 'WHO'

        if 'what' in q:
            pos = q.find('what')
            if pos < type_pos:
                type_pos = pos
                self.type = 'WHAT'
            else:
                self.support_type = 'WHAT'

        if 'when' in q:
            pos = q.find('when')
            if pos < type_pos:
                type_pos = pos
                self.type = 'WHEN'
            else:
                self.support_type = 'WHEN'

        if 'where' in q:
            pos = q.find('where')
            if pos < type_pos:
                type_pos = pos
                self.type = 'WHERE'
            else:
                self.support_type = 'WHERE'

        if 'why' in q:
            pos = q.find('why')
            if pos < type_pos:
                type_pos = pos
                self.type = 'WHY'
            else:
                self.support_type = 'WHY'

        if 'how' in q:
            if self.type != 'MEASURE':
                pos = q.find('how')
                if pos < type_pos:
                    type_pos = pos
                    self.type = 'HOW'
                else:
                    self.support_type = 'HOW'

        # If the question type word is not at the beginning of the sentence, assume that
        # any preceding words help condition the question
        if type_pos != 0:
            self.conditional = self.qstr[:type_pos]
