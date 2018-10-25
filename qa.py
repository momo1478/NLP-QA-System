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
from Questions import Questions

from copy import deepcopy

stories = []
question_sets = []

inp = []
with open(sys.argv[1]) as f:
    inp = f.readlines()

# Get our stories and question sets from the designated files
path = inp[0].strip('\n')
for i in range(1, len(inp)):
    # Build the story
    stories.append(Story(path, inp[i].strip('\n')))

    # Build the question set
    question_sets.append(Questions(path, inp[i].strip('\n')))

# Implement a really dumb QA system by checking sentence overlap
for i in range(len(stories)):
    for q in question_sets[i].questions:
        sentences = deepcopy(stories[i].sentences)

        for s in sentences:
            overlap = 0
            for word in q.words:
                if word in s.sentence:
                    overlap += 1
            s.score = overlap

        # Sort for highest score with shortest sentence
        sentences.sort(key=(lambda x: len(x.sentence)), reverse=False)
        sentences.sort(key=(lambda x: x.score), reverse=True)

        print("QuestionID: {}".format(q.qid))
        print("Answer: {}\n".format("" if sentences[0].score == 0 else " ".join(sentences[0].sentence)))


