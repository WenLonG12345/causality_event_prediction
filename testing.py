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


from stanfordcorenlp import StanfordCoreNLP

nlp = StanfordCoreNLP(r'D:\Downloads\stanford-corenlp-latest\stanford-corenlp-4.0.0')

sentence = 'lack of communication between translink and event organizers'
# sentence = 'a disruption in bus service in gold coast'

dependency_parse = nlp.dependency_parse(sentence)
print(dependency_parse)

nlp.close() 