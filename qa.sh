#!/usr/bin/bash

#source ./env/bin/activate
#python qa.py $1

pip install --user virtualenv
mkdir env
python -m virtualenv env
source ./env/bin/activate
pip install spacy
python -m spacy download en
pip install nltk
python qa.py $1
