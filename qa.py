# qa.py
#
# TODO: Add program description here
#
# Author[s]:
#   Monish Gupta
#   Paul C Carlson
# Class: CS 5340 - Fall 2018
# Date: 19 October 2018
#


import sys
from Story import Story
from QuestionSet import QuestionSet

from copy import deepcopy

inp = []
# Get the story ids
with open(sys.argv[1]) as f:
    inp = f.readlines()

# Get our stories and question sets and do sentence overlap
path = inp[0].strip('\n')
for i in range(1, len(inp)):
    # Get the story
    story = Story(path, inp[i].strip('\n'))

    # Get the question set
    question_set = QuestionSet(path, inp[i].strip('\n'))

    # Implement a really dumb QA system by checking sentence overlap
    # get the answer for each question in the question set that has the highest score
    # TODO: Decide if we want a separate class to handle scoring answers ...
    for q in question_set.questions:
        sentences = deepcopy(story.sentences)
        # Score the sentences
        for s in sentences:
            overlap = 0
            for word in q.words:
                if word in s.sentence:
                    overlap += 1
            s.score = overlap

        # Sort for highest score with shortest sentence
        sentences.sort(key=(lambda x: len(x.sentence)), reverse=False)
        sentences.sort(key=(lambda x: x.score), reverse=True)

        # Print out the QA result
        print("QuestionID: {}".format(q.qid))
        #print("Question: {}\nQType: {}".format(q.qstr, q.type))
        print("Answer: {}\n".format("" if sentences[0].score == 0 else " ".join(sentences[0].sentence)))
