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
from Story import Sentence
from QuestionSet import QuestionSet

from copy import deepcopy

import spacy

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

    #print(story.sentences)

    for q in question_set.questions:
        sentences = list(story.sentences)
        
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(unicode(q.qstr))
        verbs_in_question = [ (token.text,token.lemma_) for token in doc if token.pos_ == "VERB" and token.lemma_ not in ["be","do","have"]]
        print("Question Lemmas: {}".format(verbs_in_question))
   
        # candidate_responses = []
        # Score the sentences
        for s in sentences:
            overlap = 0
            for word in q.words:
                if word in s.sentence.split(' '):
                    overlap += 1

            for vq in verbs_in_question:
                if vq in s.lemmas:
                    overlap += 1.345654

            s.score = overlap
            #print("Sentence Lemmas: {}".format(verbs_in_sentence))
            #print("SCORE " + str(s.score))
            #print("OLD METHOD : {}".format(len(set(q.words).intersection(set(s.sentence.split())))))

            # new_candidate = q.words.intersection(s.sentence)
            # score = len(new_candidate)
            # candidate_responses.append(Sentence(new_candidate, score))

        print(sentences)

        # Sort for highest score with shortest sentence
        sentences.sort(key=(lambda x: len(x.sentence)), reverse=False)
        sentences.sort(key=(lambda x: x.score), reverse=True)
        # candidate_responses.sort(key=(lambda x: len(x.sentence)), reverse=False)
        # candidate_responses.sort(key=(lambda x: x.score), reverse=True)

        # Print out the QA result
        print("QuestionID: {}".format(q.qid))
        #print("Question: {}\nType: {}\nSupport Type: {}\nConditional: {}".format(q.qstr, q.type, q.support_type, q.conditional))
        print("Answer: {}\n".format("" if sentences[0].score == 0 else "".join(sentences[0].sentence)))
        # print("Answer: {}\n".format("" if candidate_responses[0].score == 0
        #                             else " ".join(candidate_responses[0].sentence)))
