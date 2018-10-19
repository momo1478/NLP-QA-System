import sys
from Story import Story

stories = []

inp = []
with open(sys.argv[1]) as f:
    inp = f.readlines()

path = inp[0].strip('\n')
for i in range(1,len(inp)):
    stories.append(Story())

    with open( path + inp[i].strip('\n') + ".story" ) as story:
        for line in story:
            if(line.startswith("HEADLINE:")):
                stories[i-1].headline = " ".join(line.strip('\n').split(' ')[1:])
            elif(line.startswith("DATE:")):
                stories[i-1].date = " ".join(line.strip('\n').split(' ')[1:])
            elif(line.startswith("STORYID:")):
                stories[i-1].id = " ".join(line.strip('\n').split(' ')[1:])
            else:
                stories[i-1].words += line.strip("\n").split(" ")[1:]

for story in stories:
    print("H : " + str(story.headline))
    print("D : " + story.date)
    print("ID : " + story.id)
    print("Story : " + str(story))