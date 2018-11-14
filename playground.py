import nltk
from nltk.corpus import wordnet as wn

#import spacy
from spacy.tokens import Span

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

# def spacyTest():
#     nlp = spacy.load('en_core_web_sm')
#     doc = nlp(u'''A middle school in Liverpool, Nova Scotia is pumping up bodies as wellas minds. It\'s an example of a school teaming up with the community to raisemoney. South Queens Junior High School is taking aim at the fitness market.The school has turned its one-time metal shop - lost to budget cuts almost two years ago - into a money-making professional fitness club. The club will be open seven days a week.The club, operated by a non-profit society made up of school and community volunteers, has sold more than 30 memberships and hired a full-time co-ordinator .Principal Betty Jean Aucoin says the club is a first for a Nova Scotia public school. She says the school took it on itself to provide a service needed in Liverpool.\"We don't have any athletic facilities here on the South Shore of Nova Scotia, so if we don't use our schools, communities such as Queens are going to be struggling to get anything going,\" Aucoin said.More than a $100,000 was raised through fund-raising and donations from government, Sport Nova Scotia, and two local companies.Some people are wondering if the ties between the businesses and the school are too close. Schools are not set up to make profits or promote businesses. Southwest Regional School Board superintendent Ann Jones says there\'s no fear the lines between education and business are blurring.\"First call on any school facility belongs to... the youngsters in the school,\" says Ann Jones.The 12,000-square-foot club has seven aerobic machines, including treadmills, steppers, and stationary bicycles, as well as weight machines and freeweights.Memberships cost $180 a year for adults and $135 for students and seniors.Proceeds pay the salary of the centre co-ordinator and upkeep of the facility.''')
#     printList([t.text for t in doc if t.text not in [" ", "\n", ","]], "Words in Story")
#
#     printList(list(doc.noun_chunks),"Noun Chunks")
#     printList(list(doc.sents),"Sentences")
#
#     print("* * * NER[word,start_i,end_i,label] * * *")
#     for ent in doc.ents:
#         print(ent.text, ent.start_char, ent.end_char, ent.label_)

#     doc = nlp(u'Where is South Queens Junior High School located?')
    
#     print("* * * NER[word,start_i,end_i,label] * * *")
#     for ent in doc.ents:
#         print(ent.text, ent.start_char, ent.end_char, ent.label_)
#     nlp = spacy.load('en_coref_md')
#     doc = nlp(u'''A middle school in Liverpool, Nova Scotia is pumping up bodies as wellas minds. It\'s an example of a school teaming up with the community to raisemoney. South Queens Junior High School is taking aim at the fitness market.The school has turned its one-time metal shop - lost to budget cuts almost two years ago - into a money-making professional fitness club. The club will be open seven days a week.The club, operated by a non-profit society made up of school and community volunteers, has sold more than 30 memberships and hired a full-time co-ordinator .Principal Betty Jean Aucoin says the club is a first for a Nova Scotia public school. She says the school took it on itself to provide a service needed in Liverpool.\"We don't have any athletic facilities here on the South Shore of Nova Scotia, so if we don't use our schools, communities such as Queens are going to be struggling to get anything going,\" Aucoin said.More than a $100,000 was raised through fund-raising and donations from government, Sport Nova Scotia, and two local companies.Some people are wondering if the ties between the businesses and the school are too close. Schools are not set up to make profits or promote businesses. Southwest Regional School Board superintendent Ann Jones says there\'s no fear the lines between education and business are blurring.\"First call on any school facility belongs to... the youngsters in the school,\" says Ann Jones.The 12,000-square-foot club has seven aerobic machines, including treadmills, steppers, and stationary bicycles, as well as weight machines and freeweights.Memberships cost $180 a year for adults and $135 for students and seniors.Proceeds pay the salary of the centre co-ordinator and upkeep of the facility.''')
#     if(doc._.has_coref):
#         print(doc._.coref_clusters)

sysnset("bag")

#spacyTest()