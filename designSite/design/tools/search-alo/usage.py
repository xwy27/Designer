
# coding: utf-8

# In[80]:


from repo_w2v import NGramLanguageModeler,Lang
CONTEXT_SIZE = 2
EMBEDDING_DIM = 10


# In[81]:


import json
import string
import torch
import numpy as np
import random


# In[82]:


with open('./teams_search_purpose.json','r') as f:
    teams = json.load(f)


# In[83]:


teams[list(teams.keys())[0]]


# In[84]:


with open('./grams.txt','r') as f:
    grams = f.read()
english_model = Lang('english')
english_model.addSentence(grams)


# In[85]:


st = "123 ! 12 asd "
print(english_model.remove_punctuation(st).split())


# In[86]:


word2team = dict()


# In[87]:


for key in teams.keys():
    current_team = teams[key]
    search_string = current_team['title']+' '+current_team['abstract']
    search_string = english_model.remove_punctuation(search_string).lower()
    for word in search_string.split():
        if word in word2team.keys():
            if key in word2team[word].keys():
                word2team[word][key] += 1
            else:
                word2team[word][key] = 1
        else:
            word2team[word] = {key:1}


# In[88]:


with open('./word2team.json','w') as f:
    json.dump(word2team,f)


# In[89]:


with open('./word2team.json','r') as f:
    word2team_ = json.load(f)


# In[90]:


len(word2team_)


# In[91]:


model = NGramLanguageModeler(english_model.n_words, EMBEDDING_DIM,CONTEXT_SIZE)
model.load_state_dict(torch.load('search-model.pkl'))


# In[92]:


test_vec = model.embeddings(torch.tensor([english_model.word2index['cell']],dtype=torch.long)).detach().numpy()


# In[93]:


test_vec.reshape(1,-1)


# In[94]:


def cos_dist(vec1,vec2):
    return vec1.reshape(1,-1).dot(vec2.reshape(-1,1))/(np.linalg.norm(vec1)*np.linalg.norm(vec2))


# In[121]:


def two_words_cos_dist(word1,word2):
    if word1 not in english_model.word2index.keys():
        word1 = english_model.index2word[random.randint(3,len(english_model.word2index.keys()))]
    if word2 not in english_model.word2index.keys():
        word2 = english_model.index2word[random.randint(3,len(english_model.word2index.keys()))]
    vec1 = model.embeddings(torch.tensor([english_model.word2index[word1]],dtype=torch.long))                                                                        .detach().numpy()
    vec2 = model.embeddings(torch.tensor([english_model.word2index[word2]],dtype=torch.long))                                                                        .detach().numpy()
    return cos_dist(vec1,vec2)


# In[96]:


two_words_cos_dist('cell','hello')


# In[97]:


list(word2team.keys())[:10]


# In[113]:


def word2dist(word):
    dists = []
    for __word in list(word2team.keys()):
        dists.append([two_words_cos_dist(word,__word)[0][0],__word])
    return dists


# In[165]:


def find_max_related_words(word,max_number=1):
    dists = word2dist(word)
    return list(map(lambda li:li[1],sorted(dists,key=lambda tu:tu[0],reverse=True)[:max_number]))

def find_max_related_teams(word,max_number=1):
    words = find_max_related_words(word,max_number=max_number)
    team_selected = {}
    for index in range(len(words)):
        word = words[index]
        teams4word = word2team[word]
        for team in teams4word.keys():
            if team in team_selected.keys():
                team_selected[team] += word2team[word][team]/(index+1)
            else:
                team_selected[team] = word2team[word][team]/(index+1)
    team_n_occurence = [[team,team_selected[team]]for team in team_selected.keys()]
    team_n_occurence = sorted(team_n_occurence,key=lambda te:te[1],reverse=True)
    return team_n_occurence[:max_number]


# In[166]:


find_max_related_teams('cell')


# In[169]:


def search_eng(sentence):
    words = english_model.remove_punctuation(sentence).lower().split()
    team_rank = {}
    for index in range(len(words)):
        word = words[index]
        team_n_occur_has_word = list(map(lambda li:[li[0],li[1]],find_max_related_teams(word,max_number=10)))
        for team_tuple in team_n_occur_has_word:
            if team_tuple[0] in team_rank.keys():
                team_rank[team_tuple[0]] += int(team_tuple[1])/(index+1)
            else:
                team_rank[team_tuple[0]] = int(team_tuple[1])/(index+1)
    team_tu = [[index,team_rank[index]]for index in team_rank]
    team_tu = sorted(team_tu,key=lambda te:te[1],reverse=True)
    return list(map(lambda team:teams[team[0]],team_tu[:10]))


# In[171]:


search_eng('cell rna dna')

