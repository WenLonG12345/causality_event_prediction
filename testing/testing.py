# import spacy
# from spacy import displacy

# # lack of communication between translink and event organizers.
# # A disruption in bus service in Gold Coast
# nlp = spacy.load("en_core_web_lg")
# doc = nlp("lack of communication between translink and event organizers")
# # new = ""


# # for tok in doc:
# #     if not tok.is_stop:
# #         new += tok.text + " "

# # print(new)


# displacy.serve(doc, style='dep')


# from stanfordcorenlp import StanfordCoreNLP

# nlp = StanfordCoreNLP(r'D:\Downloads\stanford-corenlp-latest\stanford-corenlp-4.0.0')

# sentence = 'lack of communication between translink and event organizers'
# # sentence = 'a disruption in bus service in gold coast'

# dependency_parse = nlp.dependency_parse(sentence)
# print(dependency_parse)

# nlp.close() 

# cause_data = ['lack communication translink event organizers ', 'philippines won arbitration case china disputed south china sea ', 'china island reclamation following claim cent sea dash line ']
# effect_data = ['disruption bus service gold coast ', 'philippine rodrigo duterte called cabinet meeting ', 'south china sea dispute security issues east asia tensions boiling ']

# tokenized_cause = []
# tokenized_effect = []

# for cause in cause_data:
#     tokenized_cause.append(cause.split())

# for effect in effect_data:
#     tokenized_effect.append(effect.split())

# bag = []

# for index in range(len(tokenized_cause)):
#     bag = []
#     for c_word in tokenized_cause[index]:
#         for e_word in tokenized_effect[index]:
#             bag.append((c_word, e_word))
    
#     print(bag)

# def max(data_list):
#     for index, value in data_list:
#         if value > max_value:
#             max_value = value
#             max_index = index
    
#     return max_value, max_index

