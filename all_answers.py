# all_answers.py

import sys

inp = []
# Get the story ids
with open(sys.argv[1]) as f:
    inp = f.readlines()

# get all answers
path = inp[0].strip('\n')

with open("all_answers.answers", 'w+') as all_answer_file:
    for i in range(1, len(inp)):
        answer_path = "{}{}.answers".format(path, inp[i].strip('\n'))

        with open(answer_path) as answer_file:
            for line in answer_file:
                all_answer_file.write(line)
