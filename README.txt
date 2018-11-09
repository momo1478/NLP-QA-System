Monish Gupta
Paul C Carlson
Professor Ellen Riloff
CS 5340 - Fall 2018

Final Project: Question Answering

Uses Python 2.7
Tested on CADE Machine: lab2-5.eng.utah.edu

Timing for single story:
  # TODO: Answer this question

External Resources:
  spaCy
    https://spacy.io/usage/

  Model: en_core_web_sm
    https://spacy.io/models/en

  Installed and run using the following commands:
    python -m pip install -U virtualenv
    virtualenv .env
    source .env/bin/activate
    pip install -U spacy
    python -m spacy download en_core_web_sm


Contributions:
  Monish:
    - Read in stories
    - spaCy setup and installation
    - Model installation
    - identified useful spaCy features:
      - NER labels
      - Sentence Splitting
      - NP Chunking
      - POS Tagging
    - Answer reduction by near word matching

  Paul:
    - Read in questions
    - Simple overlap implementation
    - Output formatting
    - Question typing
    - Named Entity to Q-Type matching for precision increase
    - Overlap with word lemma (stemming) and set intersection
    - Stop words
    - Sentence ranking


Known issues:
  May not run on other systems under other users, cause virtualenv pathing



Checkpoint 1:
- Approach 1: Simple question/answer overlap - just getting started
    - Issues:
        No question typing
        Poor sentence division
-

Checkpoint 2: Goals
- See if we can use the difficulty of the question as a heuristic when searching for
    answers (shorter or longer responses)
- Co-reference resolution
- Difficult Question types (WHAT, HOW, WHY)
