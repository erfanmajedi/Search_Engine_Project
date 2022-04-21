import json
from pydoc import doc
from re import L
from hazm import *
from matplotlib.pyplot import prism
from parsivar import Normalizer
from parsivar import Tokenizer
from parsivar import FindStems
import string
class Doc : 
    def __init__(self , docId, token) :
        self.count = 0 
        self.docId = docId
        self.token = token
        self.positions = []
    
    def insert(self, position) :
        self.count += 1
        self.positions.append(position)
        self.positions = sorted(self.positions)

class Term :
    def __init__(self , id):
        self.count = 0 
        self.id = id
        self.docTerms = dict()

    def insert(self, docId, position):
        self.count += 1
        if docId not in self.docTerms.keys():
            self.docTerms[docId] = Doc(docId, self.id)
        self.docTerms[docId].insert(position = position)


dictionary = []
# docid haye moshtarak kalameye aval v dovom ra bedast avardim 
def moshtarak(docidList1, docidList2):
    intersect = []
    for i in range(len(docidList1)) :
        for j in range(len(docidList2)) :
            if docidList1[i] == docidList2[j] :
                intersect.append(docidList1[i])
    return intersect
# inja docid kalameye dovom ba kalamat 2 be ba'ad ra hesab kardim 
def new_moshtarak(inter, tokenlist):
    for i in range(2,len(tokenlist)):
        general_docid_list = []
        for word in dictionary :
            if tokenlist[i] == word.id : 
                documentID = word.docTerms.keys()
                for j in documentID :
                    general_docid_list.append(j)
        inter = moshtarak(inter, general_docid_list)
    # for doc in inter:
    #     print(doc)          

# inja ma docid kalameye aval v dovom ro dar miarim 
def generate_doc_list(token) :
    list1 = []
    list2 = []
    word0 = token[0]
    word1 = token[1]
    for first_word in dictionary :
        if word0 == first_word.id :
            first = first_word.docTerms.keys()
            for key1 in first :
                list1.append(key1)
    for second_word in dictionary : 
        if word1 == second_word.id :
            second = second_word.docTerms.keys()
            for key2 in second :
                list2.append(key2)
    # moshtarak_id = moshtarak(list1, list2)
    # new_moshtarak(moshtarak_id,token)

def ranking(tokenlist):
    list_khali = dict()
    for i in range(0,len(tokenlist)):
        for word in dictionary :
            if tokenlist[i] == word.id : 
                documentID = word.docTerms.keys()
                for j in documentID :
                    if j not in list_khali :
                        list_khali[j] = len(tokenlist)
                    else :
                        list_khali[j] -= 1
    result = dict(sorted(list_khali.items(), key=lambda item: item[1]))
    # for key in result.keys() :
    #     print("docID:",key , "rank:" , result[key])

# # baraye do kalamei ke ! bade kalameye aval bashad
def middle_handle_mark(before_mark_tok, after_mark_tok, tokn_list):
    not_doc_list = []
    is_doc_list = []
    erfan = []
    
    for word in dictionary :
        if after_mark_tok == word.id :
            not_id = word.docTerms.keys()
            for i in not_id :
                not_doc_list.append(i)
                
            for j in range(10):
                j_ = str(j)
                if j_ not in not_doc_list :
                    erfan.append(j)
        if before_mark_tok == word.id :
            is_id = word.docTerms.keys()
            for k in is_id :
                is_doc_list.append(k)
        x = moshtarak(not_doc_list,is_doc_list)
        for i in x :
            print(i)
        new_moshtarak(x, tokn_list)
    



# inja mikhahim makane alamat ra peyda konim 
def search_mark(tkn) :
    for index in range(1,len(tkn)) :
        index_ = int(index)
        if tkn[index_] == "!" :
            middle_handle_mark(tkn[index_ - 1] ,tkn[index_ + 1], tkn)
        else :
            ranking(tkn)
    # for index in range(len(tkn)):
    #     if tkn[0] == "!" :
    #         first_handle_mark(tkn[0], tkn[index + 1])

my_list = []
def open_file() :
    with open('readme.json') as file :
        for data in file :
            datas = json.loads(data)
            my_list.append(datas)
    return my_list

my_normalizer = Normalizer(statistical_space_correction=True)
my_tokenizer = Tokenizer()
my_stemmer = FindStems()
punctuations = string.punctuation
punctuations += ''.join(['،','؟','«','»','؛'])

def positional_index(mylist):
    for list_item in my_list : 
        key = list_item.keys()
    for i in key :
        position = 0
        # words_title = my_tokenizer.tokenize_words(my_normalizer.normalize(list_item[i]['title']))
        words_content =  my_tokenizer.tokenize_words(my_normalizer.normalize(list_item[i]['content'].translate(str.maketrans('','',punctuations))))
        # words_url =  my_tokenizer.tokenize_words(my_normalizer.normalize(list_item[i]['url']))
        for j in words_content :
            stopwords = stopwords_list()
            if j not in stopwords :
                flag = 0
                position += 1
                for word in dictionary :
                    if word.id == j :
                        word.insert(i, position)
                        flag = 1
                        break
                if flag == 0 :
                    term = Term(j)
                    term.insert(i, position)
                    dictionary.append(term)


positional_index(open_file())
input = input()
mytoken = my_tokenizer.tokenize_words(input)
# generate_doc_list(mytoken)
# ranking(mytoken)
search_mark(mytoken)

