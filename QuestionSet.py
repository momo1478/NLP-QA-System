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
    measure_words = ['many', 'much', 'often', 'big', 'small', 'few', 'tall', 'long', 'short', 'heavy', 'light',
                     'fast', 'slow', 'old', 'new', 'far', 'near', 'close', 'deep']
    definition_words = ['is', 'are', 'was', 'were', 'will', 'would']

    question_types = {'WHO' : ['who', 'whom', 'whose'],
                      'WHAT' : ['what'],
                      'WHEN' : ['when'],
                      'WHERE' : ['where'],
                      'WHY' : ['why'],
                      'HOW' : ['how'],
                      'WHICH' : ['which']}

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
        q = self.qstr.replace('?', '').replace(',', '')
        self.words = [str(x).strip() for x in q.split(' ')]

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
        #
        # We will treat all questions of the form 'How <measure_words> ...'
        # the same way so detect these question types first
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

        for d in self.definition_words:
            dstr = "what {}".format(d)
            if dstr in self.qstr.lower():
                pos = self.qstr.lower().find(dstr)
                if pos < type_pos:
                    type_pos = pos
                    self.type = 'DEFINITION'
                    self.support_type = m.upper()
                else:
                    self.support_type = 'DEFINITIONs'

        for type_words in Question.question_types:
            for t in Question.question_types[type_words]:
                if t in q:
                    pos = q.find(t)
                    if pos < type_pos:
                        type_pos = pos
                        self.support_type = self.type
                        self.type = type_words
                    else:
                        self.support_type = type_words

        # If the question type word is not at the beginning of the sentence, assume that
        # any preceding words help condition the question
        if type_pos != 0:
            self.conditional = self.qstr[:type_pos]
