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

from nltk.corpus import wordnet as wn

import spacy

# need to download wordnet?
#nltk.download("wordnet")

WORD_WEIGHT = 1
VERB_WEIGHT = 10
NEAR_VERB_WEIGHT = 4
NP_WEIGHT = 5

# Q-type weights
WEIGHT_WHEN = 20
WEIGHT_WHO = 20
WEIGHT_WHO_SUPP = 0
WEIGHT_MEASURE = 20
WEIGHT_WHERE = 12
WEIGHT_WHY = 0
WEIGHT_HOW = 0
WEIGHT_WHAT = 0

# Q-NER-Labels
NER_TIME = ['TIME', 'DATE']
NER_MEASURE = ['PERCENT', 'MONEY', 'QUANTITY', 'CARDINAL']
NER_WHO = ['PERSON', 'NORP', 'ORG', 'GPE']
NER_WHERE = ['FAC', 'ORG', 'GPE', 'LOC']

# Control keys
USING_Q_TYPES = True
USING_SIMILAR_VERBS = True

ENTITY_ONLY_RESPONSE = False

NEAR_WORDS_ENABLE = False
NEAR_WORDS = 5

# Stop words: words that are probably too common to help find the right
# answer sentences
STOP_WORDS = set(['a', 'an', 'and', 'the', 'then'])
#STOP_WORDS = set(['a', 'an', 'and', 'the', 'then', 'of', 'to', 'be', 'that', 'from'])
STOP_VERBS = set(['be', 'do', 'have', 'would'])

# a an the
# he she it they them those their
# if those..:
#     of to from by that their


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

        if sys.version_info[0] >= 3:
            doc = nlp(str(q.qstr))
        else:
            doc = nlp(unicode(q.qstr))
        verbs_in_question = [(token.text, token.lemma_) for token in doc
                             if token.pos_ == "VERB" and token.lemma_ not in STOP_VERBS]

        q_ents = [token.text for token in doc.ents]

        np_chunks_in_question = [set(str(chunk).split()).difference(STOP_WORDS) for chunk in list(doc.noun_chunks)]

        # Only use question words that are not 'stop words'
        # Represent as sets to avoid double counting matching words
        qws = set([token.lemma_ for token in doc if token.lemma_ not in STOP_WORDS])

        # Get pool of similar verbs in question
        q_verb_pool = set({})
        for v in verbs_in_question:
            similar_verbs = wn.synsets(v[0], pos='v')
            for sv in similar_verbs:
                q_verb_pool = q_verb_pool.union(set(sv.lemma_names()))
        q_verb_pool = q_verb_pool.difference(set([v[0] for v in verbs_in_question]))

        # Score the sentences
        for s in sentences:
            # Add WORD_WEIGHT for every overlapping word in sentence and question
            overlap = len(qws.intersection(set(s.lemmas))) * WORD_WEIGHT

            for qnpc in np_chunks_in_question:
                for snpc in s.noun_chunks:
                    np_overlap = len(qnpc.intersection(snpc))
                    if np_overlap != 0:
                        overlap += np_overlap * NP_WEIGHT

            # Add 10 for every matching verb in both sentences
            # for vq in verbs_in_question:
            #     if vq[1] in s.lemmas:
            #         overlap += VERB_WEIGHT
            overlap += len(set([v[1] for v in verbs_in_question]).intersection(s.lemmas)) * VERB_WEIGHT

            # Trying looking for verbs that are part of the question's verbs synset
            if USING_SIMILAR_VERBS:
                overlap += len(q_verb_pool.intersection(s.lemmas)) * NEAR_VERB_WEIGHT

            if USING_Q_TYPES:
                if q.type is 'WHEN':
                    for e in s.entities:
                        if e[1] in NER_TIME:
                            overlap += WEIGHT_WHEN
                            break
                if q.type is 'MEASURE':
                    for e in s.entities:
                        if e[1] in NER_MEASURE:
                            overlap += WEIGHT_MEASURE
                            break
                if q.type is 'WHO':
                    found_who = False
                    found_supp = False
                    for e in s.entities:
                        if not found_who and e[1] is 'PERSON':
                            overlap += WEIGHT_WHO
                            found_who = True
                            #break
                        elif not found_who and (e[1] is 'NORP' or e[1] is 'ORG' or e[1] is 'GPE'):
                            overlap += WEIGHT_WHO / 2
                            found_who = True
                            #break
                        elif e[1] in NER_WHO:
                            overlap += WEIGHT_WHO_SUPP
                if q.type is 'WHERE':
                    for e in s.entities:
                        if e[1] in NER_WHERE:
                            overlap += WEIGHT_WHERE
                            break

            s.score = overlap

        # Sort for highest score with shortest sentence
        sentences.sort(key=(lambda x: len(x.sentence)), reverse=False)
        sentences.sort(key=(lambda x: x.score), reverse=True)


        if NEAR_WORDS_ENABLE:
            ans = sentences[0]
            match_indicies = [(ans.sentence.split()[i], i) for i in range(len(ans.sentence.split()))
                              if ans.sentence.split()[i] in q.qstr.split()]

            # print("* * * (match,index) * * *")
            # for mi in match_indicies:
            #     print(mi)

            final_ans = set()
            for match in match_indicies:
                index = match[1]
                lo_i = max(index-NEAR_WORDS, 0)
                hi_i = min(index+NEAR_WORDS, len(ans.sentence.split()) - 1)
                final_ans.update(ans.sentence.split()[lo_i:hi_i+1])
            
            fa = final_ans
            sentences[0].sentence = " ".join(fa) if len(fa) > 0 else sentences[0].sentence
                
        if ENTITY_ONLY_RESPONSE:
            ents_in_answer = " ".join([ents for ents in set(sentences[0].entities)])
            sentences[0].sentence = ents_in_answer if len(ents_in_answer) > 0 else sentences[0].sentence

        for i in range(len(sentences)):
            short_sent = []
            if q.type is 'WHEN':
                short_sent = [e[0] for e in sentences[0].entities if e[1] in NER_TIME]
            if q.type is 'MEASURE':
                short_sent = [e[0] for e in sentences[0].entities if e[1] in NER_MEASURE]
            if q.type is 'WHO':
                short_sent = [e[0] for e in sentences[i].entities if e[1] in NER_WHO and e[0] not in q_ents]
            if q.type is 'WHERE':
                short_sent = [e[0] for e in sentences[0].entities if e[1] in NER_WHERE and e[0] not in q_ents]

            # TODO: What am I trying to do here?
            #if q.type is 'WHAT':
                #print("Doing Nothing ...")



            if len(short_sent) != 0:
                sentences[0].sentence = " ".join(short_sent)
                break

        # Print out the QA result
        print("QuestionID: {}".format(q.qid))
        #print("Question: {}\nType: {}\nSupport Type: {}\nConditional: {}".format(q.qstr, q.type, q.support_type, q.conditional))
        print("Answer: {}\n".format("".join(sentences[-1].sentence) if sentences[0].score == 0 else "".join(sentences[0].sentence)))
        #print("Answer: {}\n".format("".join(sentences[0].sentence)))
