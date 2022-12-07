# Import the package
import numpy as np
import spacy

import os

CD_structures = { "go" : "PTRANS",
"navigate" : "PTRANS",
"walk" : "PTRANS",
"lead" : "PTRANS",
"guide" : "PTRANS",
"meet" : "PTRANS",
"follow" : "PTRANS",    #<-----------------follow me?
"bring" : "ATRANS",
"give" : "ATRANS",
"buy" : "ATRANS", #O.o?
"deliver" : "ATRANS",
"take" : "GRASP",
"find" : "ATTEND",
"look" : "ATTEND",
"open" : "PROPEL",
"push" : "PROPEL",
"pull" : "PROPEL"
    }

def CondepParser(text):
    """print("=====================================================================")
    print("|                       ORIGINAL COMMAND                            |")
    print("=====================================================================")
    print (text)"""
    
    print("=====================================================================")
    print("|                          SPACY PARSER                              |")
    print("=====================================================================")
    
    cds = []
    
    verb_list = []
    prim_list = []
    pron_list = []
    pos_list = []
    obj = []
    loc = []
#Remove the word "Robot" in order to obtain a clean separation of the types of "obj"
    text = text.replace('Robot,', '')
    
    #Extracting tokens from the sentence
    nlp = None
    try:
        nlp = spacy.load("en_core_web_sm")
    except:
        os.system("python -m spacy download en_core_web_sm")
        nlp = spacy.load("en_core_web_sm")
    
    doc = nlp(text)
    
    #Creating the list of nouns and positions
    for token in doc:
        text_list = [token.text for token in doc]
        pos_list1 = [token.pos_ for token in doc]
    print(text_list, pos_list1)
    
    pron_list = [chunk.text for chunk in doc.noun_chunks]
    pos_list = [[t.pos_ for t in chunk]for chunk in doc.noun_chunks]
    print(pron_list, pos_list)
    
    verb_list = [token.lemma_ for token in doc if token.pos_ == "VERB"]
    print(verb_list)
    
#=======================================================================
#If doesn't exist verb or nouns then send a request for a new sentece
    if len(verb_list) == 0 or len(pron_list) == 0:
        print("I can't understand you.")
    else:

    #Sentences with structures like: [NOUN]+[ADP]+[NOUN], ex: ... a glass of water
    #Sentences with structures like: [NOUM]+[CCONJ]+[NOUN], ex: ... coffee and donuts
    #These sentences need to check for two consecutive nouns in the noun_list and analize
    #the type of word between them.
        for pos in range(len(pos_list)):
            if pos_list[pos] == ["NOUN"] and pos_list[pos-1][-1] == "NOUN":
                #print("<--------------------------")
                inter = text_list[text_list.index(pron_list[pos])-1]
                #int = pos_list1[text_list.index(pron_list[pos])+1]
                
                if inter == "of":
                    new_noun = pron_list[pos-1] + " "+ inter + " " +pron_list[pos]
                    pron_list[pos-1] = new_noun
                    pron_list = np.delete(pron_list, [pos])
                    print(pron_list)
                    
                elif inter == "and":
                    v1 = pos_list1[text_list.index(pron_list[pos])-3]
                    v1_text = text_list[text_list.index(pron_list[pos])-3]
                    v2 = pos_list1[text_list.index(pron_list[pos])-4]
                    v2_text = text_list[text_list.index(pron_list[pos])-4]
                    
                    if v1 == "VERB":
                        v = verb_list.index(v1_text)
                        verb_list.insert(v+1, v1_text)
                        print(verb_list)
                        
                    elif v2 == "VERB":
                        v = verb_list.index(v2_text)
                        verb_list.insert(v+1, v2_text)
                        print(verb_list)
                    
                    #REPEAT THE PERSON
                    find_noun = pron_list.index(text_list[text_list.index(pron_list[pos])])
                    #check_noun = pos_list1[text_list.index(pron_list[find_noun-1])+4]
                    
                    #[me, milk, sugar]  ---- give me milk and sugar
                    if pos_list1[text_list.index(pron_list[find_noun-1])-1] == "PRON":
                        pron_list.insert(pos+1, text_list[text_list.index(pron_list[find_noun-1])-1])
                        print(pron_list)
                        
                    #[milk, sugar, MJ] ---- give milk and sugar to her [PRON] / Mary [PROPN]
                    elif pos_list1[text_list.index(pron_list[find_noun-1])+4] == "PROPN" or pos_list1[text_list.index(pron_list[find_noun-1])+4] == "PRON":
                        pron_list.insert(find_noun, pron_list[pos+1])
                        print(pron_list)
    
    #Sentences where "me" the recipient of the action, ex: give me ....
    #Check for the word me, which change the order of noun_list, so the word "me" is added
    #to the end of the list instead of the beggining
        s = len(pron_list)-1
        for m in range(len(pron_list)):
            if pos_list[m] == ['PRON'] and m != s:
                pron_b =  pron_list[m]
                pron_list[m] = pron_list[m+1]
                pron_list[m+1] = pron_b

    #Sentences where her o him are included, ex: ... and give an apple to her
    #Check for the words "her" or "him" and replace them with the last PROPN
        for pron in range(len(pron_list)):
            if pron_list[pron] == 'her' or pron_list[pron] == "him":
                for i in range(len(pos_list)):
                    for p in pos_list[i]:
                        if p == "PROPN": #<---------------------
                            pron_list[pron] = pron_list[i]
                            break
        
        for k in verb_list:
            prim_list = np.append(prim_list, CD_structures[k])
            #print(prim_list)
        
        print("=====================================================================")
        print("|                    CONCEPTUAL DEPENDENCIES                        |")
        print("=====================================================================")
    
    #Building the DC structure
        for k in range(len(prim_list)):
            if prim_list[k] == 'PTRANS':
                #print(prim_list[k]+'((ACTOR Robot)(OBJECT Robot) (FROM Robots place) (TO '+pron_list[0]+'))')
                cd = prim_list[k]+'((ACTOR Robot)(OBJECT Robot) (FROM Robots place) (TO '+pron_list[0]+'))'
                cds.append(cd)
                pron_list = np.delete(pron_list, 0)
            elif prim_list[k] == 'ATRANS':
                #print(prim_list[k]+'((ACTOR Robot)(OBJECT '+pron_list[0]+') (FROM '+pron_list[0]+' place) (TO '+pron_list[1]+'))')
                cd = prim_list[k]+'((ACTOR Robot)(OBJECT '+pron_list[0]+') (FROM '+pron_list[0]+' place) (TO '+pron_list[1]+'))'
                cds.append(cd)
                pron_list = np.delete(pron_list, 0)
                pron_list = np.delete(pron_list, 0)
            elif prim_list[k] == 'ATTEND':
                #print(prim_list[k]+'((ACTOR Robot)(TO '+pron_list[0]+'))')
                cd = prim_list[k]+'((ACTOR Robot)(TO '+pron_list[0]+'))'
                cds.append(cd)
                pron_list = np.delete(pron_list, 0)
            elif prim_list[k] == 'GRASP':
                #print(prim_list[k]+'((ACTOR Robot)(OBJ '+pron_list[0]+'))')
                cd = prim_list[k]+'((ACTOR Robot)(OBJ '+pron_list[0]+'))'
                cds.append(cd)
                pron_list = np.delete(pron_list, 0)
    
    return cds
