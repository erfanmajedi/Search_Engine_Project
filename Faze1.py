from copyreg import remove_extension
import json
from operator import pos
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
def new_moshtarak(inter, tokenlist, exclam_ind):
    for i in range(2,len(tokenlist)):
        general_docid_list = []
        if exclam_ind != i:
            for word in dictionary :
                if tokenlist[i] == word.id : 
                    documentID = word.docTerms.keys()
                    for j in documentID :
                        general_docid_list.append(j)
        else:
            have_term = []
            for word in dictionary :
                if tokenlist[i] == word.id : 
                    documentID = word.docTerms.keys()
                    for j in documentID :
                        have_term.append(j) 
                        for not_exclam in range(10) :
                            if not_exclam not in have_term :
                                general_docid_list.append(not_exclam)
        inter = moshtarak(inter, general_docid_list)
    # for doc in inter:
    #     print(doc)          

# inja ma docid kalameye aval v dovom ro dar miarim 
def generate_doc_list(token, exclam_ind) :
    list1 = []
    list2 = []
    complement_0 = []
    complement_1 = []
    word0 = token[0]
    if exclam_ind == 0:
        for i in dictionary :
            if word0 == i.id :
                j = i.docTerms.keys()
                for k in j :
                    list1.append(k)
                for com in range(10) :
                    com_ = str(com)
                    if com_ not in list1 :
                        complement_0.append(com_)
        list1 = complement_0                
    word1 = token[1]
    if exclam_ind == 1:
        for i in dictionary :
            if word1 == i.id :
                j = i.docTerms.keys()
                for k in j :
                    list2.append(k)
                for com in range(10) :
                    com_ = str(com)
                    if com_ not in list2 :
                        complement_1.append(com_)
        list2 = complement_1                
    if exclam_ind != 0 or exclam_ind != 1 :
        if exclam_ind != 0:
            for first_word in dictionary :
                if word0 == first_word.id :
                    first = first_word.docTerms.keys()
                    for key1 in first :
                        list1.append(key1)
        if exclam_ind != 1:                
            for second_word in dictionary : 
                if word1 == second_word.id :
                    second = second_word.docTerms.keys()
                    for key2 in second :
                       list2.append(key2)
    """print("list1")                
    for elem_1 in list1:
        print(elem_1)
    print("list2")                
    for elem_2 in list2:
        print(elem_2) """                    
    moshtarak_id = moshtarak(list1, list2)
    new_moshtarak(moshtarak_id,token,exclam_ind)

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
        
def not_kalame(word) :
    not_list = []
    complement = []
    for i in dictionary :
            if word == i.id :
                j = i.docTerms.keys()
                for k in j :
                    not_list.append(k)
                for com in range(10) :
                    com_ = str(com)
                    if com_ not in not_list :
                        complement.append(com_)
    return complement

def handle_mark(tokn_list):
    exclam_index = -1
    for token in range(len(tokn_list)) :
        if tokn_list[token] == "!" :
            tokn_list.remove("!")
            exclam_index = token
            break
    if len(tokn_list) == 1:
        complement = not_kalame(tokn_list[0])
        for element in complement:
            print(element) 
    else:       
        generate_doc_list(tokn_list, exclam_index)   

def quotation_handle(without_quotation_token_list, quo_mark) :
    q_flag = 0
    quo_list1 = []
    quo_list2 = []
    for word in dictionary :
        for not_quotation_token in without_quotation_token_list :
            if not_quotation_token == word.id : 
                if quo_mark == 1 :
                    quo_list1 = quo_list2
                    quo_list1 = []
                    for position in list(word.docTerms.values()) :
                        if q_flag == 0 :
                            quo_list1.append(position)
                        else :
                            for element in quo_list2:
                                if position.id == element.id:
                                    for item1 in list(position.docTerms.values()):
                                        for item2 in list(element.docTerms.values()):
                                            if (item1 - 1) == item2:
                                                quo_list1.append(position)
    # for i in quo_list1 :
    #     print(i.docId)                                                   
   
                                          
def delete_quotation(my_token_list):
    # alamat quote darim 
    quotation_mark = 0 
    without_quotation_list = []
    for word in my_token_list :
        for character in range(len(word)) :
            if word[character] == '"' :
                w = list(word)
                w.remove(word[character])
                # alamate quote remove shod 
                quotation_mark = 1
        w_string = "".join(w)
        without_quotation_list.append(w_string)
    quotation_handle(without_quotation_list, quotation_mark)


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
    for list_item in mylist : 
        key = list_item.keys()
    for i in key :
        position = 0
        # words_title = my_tokenizer.tokenize_words(my_normalizer.normalize(list_item[i]['title']))
        words_content =  my_tokenizer.tokenize_words(my_normalizer.normalize(list_item[i]['content'].translate(str.maketrans('','',punctuations))))
        # words_url =  my_tokenizer.tokenize_words(my_normalizer.normalize(list_item[i]['url']))
        for j in words_content :
            j = my_stemmer.convert_to_stem(j)
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
delete_quotation(mytoken)
# generate_doc_list(mytoken)
# ranking(mytoken)
# handle_mark(mytoken)

