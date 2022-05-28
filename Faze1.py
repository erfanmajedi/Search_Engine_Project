from ast import In
import json
import matplotlib.pyplot as plt
from hazm import stopwords_list
import numpy as np
from parsivar import Normalizer
from parsivar import Tokenizer
from parsivar import FindStems
import string
from collections import Counter
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
    # for i in inter :
    #     print(i)

    # inter = [key for key, value in Counter(inter).most_common()]    
    # for item in inter:
    #     with open("IR_data_news_12k.json", "r") as file:
    #         jsonObject = json.load(file)
    #         print(item)
    #         print(jsonObject[item]["url"])
    #         print(jsonObject[item]["title"])
    #         file.close()                                          
                            
                 

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
        
# def not_kalame(word) :
#     not_list = []
#     complement = []
#     for i in dictionary :
#             if word == i.id :
#                 j = i.docTerms.keys()
#                 for k in j :
#                     not_list.append(k)
#                 for com in range(10) :
#                     com_ = str(com)
#                     if com_ not in not_list :
#                         complement.append(com_)
#     return complement

# def handle_mark(tokn_list):
#     exclam_index = -1
#     for token in range(len(tokn_list)) :
#         if tokn_list[token] == "!" :
#             tokn_list.remove("!")
#             exclam_index = token
#             break
#     if len(tokn_list) == 1:
#         complement = not_kalame(tokn_list[0])
#         for element in complement:
#             print(element) 
#     else:       
#         generate_doc_list(tokn_list, exclam_index)   


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

def counter(word):
  return word.count

def zipf() :
    # with open('readme.json') as file : 
    #     for object in file :
    #         objects = json.loads(object)
    #         zipf_list.append(objects)
    #         for elem in zipf_list :
    #             content = my_tokenizer.tokenize_words(my_normalizer.normalize(zipf_list[elem]['content'].translate(str.maketrans('','',punctuations))))
    mehvareX = []
    mehvareY = []
    storage = dictionary
    storage.sort(key = counter, reverse = True)
    # for word in storage :
    #     print(word.count, word.id)
    for wordCounter in range(1, len(dictionary) + 1) :
        mehvareX.append(np.log(wordCounter))
    for wordFreq in storage :
        mehvareY.append(np.log(wordFreq.count))
    plt.title("Zipf Law")
    plt.plot(mehvareX, mehvareY)
    # plt.show()

def heap(all_tokens, all_words) : 
    # print(all_tokens)
    # print(all_words)
    plt.plot(np.log(all_tokens), np.log(all_words))
    # plt.show()
 
my_normalizer = Normalizer(statistical_space_correction=True)
my_tokenizer = Tokenizer()
my_stemmer = FindStems()
punctuations = string.punctuation
punctuations += ''.join(['،','؟','«','»','؛'])

def positional_index(mylist):
    length_words_content = []
    length_all_the_words = []
    cumulative_sum_words = 0
    for list_item in mylist : 
        key = list_item.keys()
    for i in key :
        # print(i)
        position = 0
        # words_title = my_tokenizer.tokenize_words(my_normalizer.normalize(list_item[i]['title']))
        words_content =  my_tokenizer.tokenize_words(my_normalizer.normalize(list_item[i]['content'].translate(str.maketrans('','',punctuations))))
        if i == '500' or i == '1000' or i == '1500' or i == '2000' :
            cumulative_sum_words += len(words_content)
            length_words_content.append(cumulative_sum_words)
        # all_the_words = dictionary
        # words_url =  my_tokenizer.tokenize_words(my_normalizer.normalize(list_item[i]['url']))
        for j in words_content :
            j = my_stemmer.convert_to_stem(j)
            stopwords = set(stopwords_list())
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
        if i == '500' or i == '1000' or i == '1500' or i == '2000' :
            length_all_the_words.append(len(dictionary))
    heap(length_words_content, length_all_the_words)


def tf_idf_query() : 
    query = input()
    N = 10 
    flag = 0
    tf_of_each_doc = []
    for word in dictionary : 
        if query == word.id : 
            # print(word.id)
            idf = np.log10(N/len(list(word.docTerms.keys())))
            for key in word.docTerms.keys() : 
                tf = len(word.docTerms[key].positions)
                tf_of_each_doc.append(tf)
    # print(tf_of_each_doc)
    for tf in tf_of_each_doc :
        if tf == 0 : 
            flag = 1
            break
        if flag == 0 : 
            term_frequecy = 1 + np.log10(tf)
        weight = term_frequecy * idf 
        # print(weight)
            # print(term_frequecy)
    # print(len(list(word.docTerms.keys())))
    # print(idf)

def tf_idf_document() :
    N = 10
    document_vector = [ [] for i in range(N)]
    for word in dictionary :
        doc_iter = [0] * N
        doc_num = len(list(word.docTerms.keys()))
        idf = np.log10(N / doc_num)
        print(word.id, idf)
        for key in word.docTerms.keys() :
            doc_iter[int(key)] = 1
            #print(word.id, key)
            frequency = len(word.docTerms[key].positions)
            tf = 1 + np.log10(frequency)
            # print("doc_id", key, "tf:" ,tf)
            weight = tf * idf 
            pair = (word.id , weight)
            document_vector[int(key)].append(pair)
        for i in range(N):
            if doc_iter[i] == 0:
                document_vector[i].append((word.id, 0.0))
    print(document_vector[0])
        

    



    

        
    
            
    

    
        
    
text = open_file()
positional_index(text)
# zipf()
# heap()
# input = input()
# mytoken = my_tokenizer.tokenize_words(input)
# tf_idf_query()
tf_idf_document()
# delete_quotation(mytoken)
# generate_doc_list(mytoken, -1)
# ranking(mytoken)
# handle_mark(mytoken)
