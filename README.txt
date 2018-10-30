Monish Gupta
Paul C Carlson
Professor Ellen Riloff
CS 5340 - Fall 2018

Final Project: Question Answering

Uses Python3
Tested on CADE Machine: ?

Known issues:

Tools/Architecture:
- To Find:
    - Sentence Splitter
    - POS tagger
    - NER system
        - For identifying answers
        - For understanding questions ...
    - Semantic Analyzer ...
    - Query Expansion?
    - Stemming?
    - Coreference resolution

    - WordNet

- To Build:
    - Question Typer
    - Answer recognizer

- Required Packages:
	- (pip install) virtualenv
        - python3 -m virtualenv env (linux)
        - py -m virtualenv env
    - (pip install) spacy
        - python -m spacy download en_core_web_sm

Checkpoint 1:
- Approach 1: Simple question/answer overlap - just getting started
    - Issues:
        No question typing
        Poor sentence division

- Can we use the difficulty of the question as a heuristic when searching for
    answers?

Checkpoint 2:
