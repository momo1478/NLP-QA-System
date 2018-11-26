import nltk
from nltk.corpus import wordnet as wn

import spacy
from spacy.tokens import Span

import sys

def printList(l, name = "*"):
    print("* * * " + name + " * * *")
    for e in l:
        print(e)

def sysnset(word):
    # ----- Only need to download once! ------#
    #nltk.download("wordnet")
    synonyms = wn.synsets(word, pos='v')
    ss = set({})
    for s in synonyms:
        sleep = s.lemma_names()
        #print(set(sleep))
        ss = ss.union(set(sleep))
    print(ss)

def spacyTest():
    nlp = spacy.load('en_core_web_sm')
    #doc = nlp(u'''is are was were would do does did has''')
    #doc = nlp(u'Where is South Queens Junior High School located?')
    #doc = nlp(u'In Turkey, police have reportedly arrested hundreds of supporters of the main Kurdish party, while up to 4,000 soldiers have been sent into Northern Iraq to attack Kurdish rebel bases.')
    doc = nlp(u'Doctors say that Tyrell Dueck, 13, will die from cancer in less than a year if he doesn t have part of his thigh bone removed and undergo chemotherapy treatments.')
    for word in doc:
        print('{}, {}, {}'.format(word.text, word.pos_, word.dep_))

    #doc = nlp(u'''A middle school in Liverpool, Nova Scotia is pumping up bodies as wellas minds. It\'s an example of a school teaming up with the community to raisemoney. South Queens Junior High School is taking aim at the fitness market.The school has turned its one-time metal shop - lost to budget cuts almost two years ago - into a money-making professional fitness club. The club will be open seven days a week.The club, operated by a non-profit society made up of school and community volunteers, has sold more than 30 memberships and hired a full-time co-ordinator .Principal Betty Jean Aucoin says the club is a first for a Nova Scotia public school. She says the school took it on itself to provide a service needed in Liverpool.\"We don't have any athletic facilities here on the South Shore of Nova Scotia, so if we don't use our schools, communities such as Queens are going to be struggling to get anything going,\" Aucoin said.More than a $100,000 was raised through fund-raising and donations from government, Sport Nova Scotia, and two local companies.Some people are wondering if the ties between the businesses and the school are too close. Schools are not set up to make profits or promote businesses. Southwest Regional School Board superintendent Ann Jones says there\'s no fear the lines between education and business are blurring.\"First call on any school facility belongs to... the youngsters in the school,\" says Ann Jones.The 12,000-square-foot club has seven aerobic machines, including treadmills, steppers, and stationary bicycles, as well as weight machines and freeweights.Memberships cost $180 a year for adults and $135 for students and seniors.Proceeds pay the salary of the centre co-ordinator and upkeep of the facility.''')
    clauses = [doc[word.left_edge.i: word.right_edge.i + 1].text for word in doc if word.dep_ in ('nsubj')]
    printList(clauses)
    # for word in doc:
    #     if word.dep_ in ('advcl'):
    #         subtree_span = doc[word.left_edge.i: word.right_edge.i + 1]
    #         print(subtree_span.text, '|', subtree_span.root.text)
            #print(' '.join([w.text for w in word.subtree]))
    # doc = nlp('''What do anti-smoking organizations think about the cigarette packaging plan? Anti-smoking organizations have applauded the strategy. The Non-Smokers Rights Association says the labels will give people a graphic reminder of the harmful effects of smoking a cigarette.''')
    # printList([t.text for t in doc if t.text not in [" ", "\n", ","]], "Words in Story")
    #
    # printList(list(doc.noun_chunks),"Noun Chunks")
    # printList([(t.text, t.lemma_, t.tag_, t.pos_, t.dep_) for t in doc], "Sentences")
    # printList([(e.text, e.label_) for e in doc.ents])
    # for chunk in doc.noun_chunks:
    #     print(chunk.text, chunk.root.text, chunk.root.dep_,
    #           chunk.root.head.text)
#
#     print("* * * NER[word,start_i,end_i,label] * * *")
#     for ent in doc.ents:
#         print(ent.text, ent.start_char, ent.end_char, ent.label_)
    
#     print("* * * NER[word,start_i,end_i,label] * * *")
#     for ent in doc.ents:
#         print(ent.text, ent.start_char, ent.end_char, ent.label_)
#     nlp = spacy.load('en_coref_md')
#     doc = nlp(u'''A middle school in Liverpool, Nova Scotia is pumping up bodies as wellas minds. It\'s an example of a school teaming up with the community to raisemoney. South Queens Junior High School is taking aim at the fitness market.The school has turned its one-time metal shop - lost to budget cuts almost two years ago - into a money-making professional fitness club. The club will be open seven days a week.The club, operated by a non-profit society made up of school and community volunteers, has sold more than 30 memberships and hired a full-time co-ordinator .Principal Betty Jean Aucoin says the club is a first for a Nova Scotia public school. She says the school took it on itself to provide a service needed in Liverpool.\"We don't have any athletic facilities here on the South Shore of Nova Scotia, so if we don't use our schools, communities such as Queens are going to be struggling to get anything going,\" Aucoin said.More than a $100,000 was raised through fund-raising and donations from government, Sport Nova Scotia, and two local companies.Some people are wondering if the ties between the businesses and the school are too close. Schools are not set up to make profits or promote businesses. Southwest Regional School Board superintendent Ann Jones says there\'s no fear the lines between education and business are blurring.\"First call on any school facility belongs to... the youngsters in the school,\" says Ann Jones.The 12,000-square-foot club has seven aerobic machines, including treadmills, steppers, and stationary bicycles, as well as weight machines and freeweights.Memberships cost $180 a year for adults and $135 for students and seniors.Proceeds pay the salary of the centre co-ordinator and upkeep of the facility.''')
#     if(doc._.has_coref):
#         print(doc._.coref_clusters)

# sysnset("bag")

spacyTest()
# nlp = spacy.load('en_core_web_sm')
# for q in sys.stdin:
#    doc = nlp(unicode(q))
#    for token in doc:
#       if(str(token) != '\n'):
#           print(str(token),str(token.dep_))
#    print("")

# avg = 0
# count = 0
# for a in sys.stdin:
#     sp = a.split('|')
#     for ans in sp:
#         print(len(ans.split(' ')))
#         avg += len(ans.split(' '))
#         count+= 1
# print("Average ans length " + str(int(avg/count)))
