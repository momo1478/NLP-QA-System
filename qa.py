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

WORD_WEIGHT = 1
VERB_WEIGHT = 10
NEAR_VERB_WEIGHT = 6
NP_WEIGHT = 0

ENTITY_ONLY_RESPONSE = False

NEAR_WORDS_ENABLE = False
NEAR_WORDS = 100
# Stop words
STOP_WORDS = set(['a', 'an', 'and', 'the', 'then'])
STOP_VERBS = set(['be', 'do', 'have', 'would'])

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

    # Implement a really dumb QA system:
    #   Score by:
    #       sentence overlap
    #       matching verbs
    #   Return the sentence that has the highest resulting score
    #
    # TODO: Decide if we want a separate class to handle scoring answers ...
    for q in question_set.questions:
        sentences = deepcopy(list(story.sentences))

        nlp = spacy.load('en_core_web_sm')
        if sys.version_info[0] > 3:
            doc = nlp(str(q.qstr))
        else:
            doc = nlp(unicode(q.qstr))
        verbs_in_question = [(token.text, token.lemma_) for token in doc
                             if token.pos_ == "VERB" and token.lemma_ not in STOP_VERBS]

        np_chunks_in_question = [set(str(chunk).split()).difference(STOP_WORDS) for chunk in list(doc.noun_chunks)]

        # Only use question words that are not 'stop words'
        # Represent as sets to avoid double counting matching words
        #qws = set([w for w in q.words if w not in STOP_WORDS])
        qws = set([token.lemma_ for token in doc if token.lemma_ not in STOP_WORDS])

        # Score the sentences
        for s in sentences:
            # Add WORD_WEIGHT for every overlapping word in sentence and question
            #overlap = len(qws.intersection(set(s.sentence.split(' ')))) * WORD_WEIGHT
            overlap = len(qws.intersection(set(s.lemmas))) * WORD_WEIGHT
            #overlap = 0

            for qnpc in np_chunks_in_question:
                for snpc in s.noun_chunks:
                    np_overlap = len(qnpc.intersection(snpc))
                    if np_overlap != 0:
                        #print("Question: {} Sentence: {}".format(qnpc, snpc))
                        overlap += np_overlap * NP_WEIGHT

            # Add 1 for every matching word in the question and sentence
            # for word in q.words:
            #     if word in s.sentence.split(' '):
            #         overlap += WORD_WEIGHT

            # Add 10 for every matching verb in both sentences
            for vq in verbs_in_question:
                if vq[1] in s.lemmas:
                    overlap += VERB_WEIGHT

            s.score = overlap
        #print(sentences)
            #print("Sentence Lemmas: {}".format(verbs_in_sentence))
            #print("SCORE " + str(s.score))

            # new_candidate = q.words.intersection(s.sentence)
            # score = len(new_candidate)
            # candidate_responses.append(Sentence(new_candidate, score))

        # Sort for highest score with shortest sentence
        sentences.sort(key=(lambda x: len(x.sentence)), reverse=False)
        sentences.sort(key=(lambda x: x.score), reverse=True)
        
        if(NEAR_WORDS_ENABLE):
            ans = sentences[0]
            match_indicies = [(ans.sentence.split()[i],i) for i in range(len(ans.sentence.split())) if ans.sentence.split()[i] in q.qstr.split()]

            # print("* * * (match,index) * * *")
            # for mi in match_indicies:
            #     print(mi)

            final_ans = set()
            for match in match_indicies:
                index = match[1]
                lo_i = max(index-NEAR_WORDS,0)
                hi_i = min(index+NEAR_WORDS,len(ans.sentence.split()) - 1)
                final_ans.update(ans.sentence.split()[lo_i:hi_i+1])
            
            fa = final_ans
            sentences[0].sentence = " ".join(fa) if len(fa) > 0 else sentences[0].sentence
                
        if ENTITY_ONLY_RESPONSE:
            ents_in_answer = " ".join([ents for ents in set(sentences[0].entities)])
            sentences[0].sentence = ents_in_answer if len(ents_in_answer) > 0 else sentences[0].sentence

        # Print out the QA result
        print("QuestionID: {}".format(q.qid))
        print("Question: {}\nType: {}\nSupport Type: {}\nConditional: {}".format(q.qstr, q.type, q.support_type, q.conditional))
        print("Answer: {}\n".format("" if sentences[0].score == 0 else "".join(sentences[0].sentence)))
        # print("Answer: {}\n".format("" if candidate_responses[0].score == 0
        #                             else " ".join(candidate_responses[0].sentence)))
