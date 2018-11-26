# all_answers.py

import sys
from QuestionSet import Question

# Q-Type specific testing:
# Q_TYPE_RUN is a list of qtypes that will be included in the answer file - this is based
# on the question types defined in QuestionSet.py
# If the first element of Q_TYPE_RUN is 'ALL' then all question types will be included
# in the file
Q_TYPE_RUN = ['WHAT']

inp = []
# Get the story ids
with open(sys.argv[1]) as f:
    inp = f.readlines()

# get all answers
path = inp[0].strip('\n')

with open(sys.argv[2], 'w+') as all_answer_file:
    first_question = True
    answer = ''
    for i in range(1, len(inp)):
        answer_path = "{}{}.answers".format(path, inp[i].strip('\n'))

        with open(answer_path) as answer_file:
            skip = False
            for line in answer_file:
                if line is '\n':
                    continue
                answer += line
                if line.startswith("Question:"):
                    q = Question(0, " ".join(line.strip('\n').split(' ')[1:]), '')
                    if Q_TYPE_RUN[0] is not 'ALL' and q.type not in Q_TYPE_RUN:
                        skip = True
                if line.startswith("Difficulty:"):
                    if not skip:
                        answer += '\n'
                        all_answer_file.write(answer)
                        last_write = 'question'
                        last_question = True

                    answer = ''
                    skip = False

