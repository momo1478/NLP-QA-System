# Story.py
#
# TODO: Add class description here
#
# Author[s]:
#   Monish Gupta
#   Paul C Carlson
# Class: CS 5340 - Fall 2018
# Date: 19 October 2018
#
import os
import spacy

class Story:
    def __init__(self, story_path, story_id):
        self.story_file_name = "{}{}.story".format(os.getcwd() + "/" + story_path, story_id)
        self.headline = ""
        self.date = ""
        self.id = story_id
        self.story = u""
        self.words = []
        self.sentences = []
        # (text, start_index, end_index, class)
        self.entities = []
        # (text, lemma, pos, tag, dependency parse, shape, is_alpha, is_stop)
        # Note : tag is more specific classification of POS ()
        self.tags = []

        # Read the story in from file
        self.__retrieve_story()

    # Return the story as it was in the original file
    def __repr__(self):
        return "HEADLINE: {}\nDATE: {}\nSTORYID: {}\n\nTEXT:\n\n{}\n".format(
            self.headline, self.date, self.id, " ".join(self.words)
        )

    # Retrieve a story from the designated file
    # Stories are of the form
    # HEADLINE: <headline>
    # DATE: <date>
    # STORYID: <id>
    #
    # TEXT:
    #
    # <story>
    def __retrieve_story(self):
        story = ""
        with open(self.story_file_name) as story_file:
            for line in story_file:
                if line.startswith("HEADLINE:"):
                    self.headline = " ".join(line.strip('\n').split(' ')[1:])
                elif line.startswith("DATE:"):
                    self.date = " ".join(line.strip('\n').split(' ')[1:])
                elif line.startswith("STORYID:"):
                    continue
                elif line.startswith("TEXT:"):
                    continue
                else:
                    story += line.replace("\n", " ")

        self.story = story
        self.__process_story(story)

    # Tokenize story for its words, sentences.
    # Parse story for its named entities and POS tags
    def __process_story(self, story):
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(str(story))
        self.words = list([t.text for t in doc if t.is_alpha or t.is_digit or t.is_currency])

        self.sentences = [Sentence(sentence.text,
                                   [token.lemma_ for token in sentence],
                                   [set(str(chunk).split()) for chunk in list(sentence.noun_chunks)])
                          for sentence in list(doc.sents)]

        self.entities = [(ent.text, ent.start_char, ent.end_char, ent.label_) for ent in doc.ents]
        self.tags = [((token.text,
                       token.lemma_,
                       token.pos_,
                       token.tag_,
                       token.dep_,
                       token.shape_,
                       token.is_alpha,
                       token.is_stop))
                     for token in doc if token.is_alpha or token.like_num]
        # print("WORDS : " + str(self.words))
        # print("SENTENCES : " + str(self.sentences))
        # print("ENTITIES : " + str(self.entities))
        # print("TAGS : " + str(self.tags))


# TODO: decide if we want an inner class for sentence representation
class Sentence:
    def __init__(self, sentence, lemmas, noun_chunks, score=0):
        self.sentence = str(sentence)
        self.noun_chunks = noun_chunks
        self.lemmas = lemmas
        self.score = score

    # Report the sentence and current score, useful for debugging
    def __repr__(self):
        return "Score: {}  Sentence: {}\n".format(
            self.score, "".join(self.sentence)
        )


# TODO: decide if we should have an 'Answer' class and if it should be separate
class Answer:
    def __init__(self, answer):
        self.answer = answer
        self.score = 0

    # Report the sentence and current score, useful for debugging
    def __repr__(self):
        return "Score: {}  Answer: {}\n".format(
            self.score, " ".join(self.answer)
        )