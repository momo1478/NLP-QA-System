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


class Story:
    def __init__(self, story_path, story_id):
        self.story_file_name = "{}{}.story".format(story_path, story_id)
        self.headline = ""
        self.date = ""
        self.id = story_id
        self.story = ""
        self.words = []
        self.sentences = []

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
        self.words = story.split(" ")[:]
        self.__split_into_sentences(story)

    # Really simple way to make sentences ... just grab words until you see a period
    # TODO: Look into finding a more intelligent sentence splitter!
    def __split_into_sentences(self, story):
        sentence_start = 0
        for i in range(len(self.words)):
            if '.' in self.words[i] and i - sentence_start > 2 \
                    or '?' in self.words[i] \
                    or '!' in self.words[i]:
                new_sentence = self.words[sentence_start:i+1]
                new_sentence[-1] = new_sentence[-1].replace('.', '')
                new_sentence = [x for x in new_sentence if x != '']
                self.sentences.append(Sentence(set(new_sentence)))
                sentence_start = i+1
        if sentence_start < len(self.words):
            self.sentences.append(Sentence(self.words[sentence_start:]))


# TODO: decide if we want an inner class for sentence representation
class Sentence:
    def __init__(self, sentence, score=0):
        self.sentence = sentence
        self.score = score

    # Report the sentence and current score, useful for debugging
    def __repr__(self):
        return "Score: {}  Sentence: {}\n".format(
            self.score, " ".join(self.sentence)
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