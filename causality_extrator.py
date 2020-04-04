import re
import spacy
import json
import pandas as pd
from nltk.corpus import wordnet as wn
from nltk.corpus import verbnet as vn


class CausalityMention():
    def __init__(self):
        pass

    '''<effect> because of|because|after <cause>'''
    def ruler1(self,sentence):
        pattern = re.compile(r'(.*)\s(because of|because|after)\s(.*)')
        result = pattern.findall(sentence)
        data = dict()
        if result:
            data['cause'] = result[0][2]
            data['effect'] = result[0][0]
        
        return data

    '''After <cause>, <effect>'''
    def ruler2(self,sentence):
        # .*? -> match min character 
        pattern = re.compile(r'^(After\s)(.*?),\s(.*)')
        result = pattern.findall(sentence)
        data = dict()
        if result:
            data['cause'] = result[0][1]
            data['effect'] = result[0][2]
        
        return data

    '''<cause> therefore|lead to|led to <effect>'''
    def ruler3(self, sentence):
        pattern = re.compile(r'(.*)\s(therefore|lead to|led to)\s(.*)')
        result = pattern.findall(sentence)
        data = dict()
        if result:
            data['cause'] = result[0][0]
            data['effect'] = result[0][2]
        
        return data


    # default dependency parse
    def sentence_segmentation(self,content):
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(content)
        sentence = list()

        for sent in doc.sents:
            sentence.append(sent.text)

        return sentence

    def extract_causalit_pair(self,sentences):
        final_result = []
        for sentence in sentences:
            if self.ruler1(sentence):
                result = self.ruler1(sentence)
            elif self.ruler2(sentence):
                result = self.ruler2(sentence)
            elif self.ruler3(sentence):
                result = self.ruler3(sentence)

            final_result.append(result)
         
                
        return final_result

    def extract_main(self,content):
        sentences = self.sentence_segmentation(content)
        print('Total sentences: ' + str(len(sentences)))

        extracted_causality_pairs = self.extract_causalit_pair(sentences)
        return extracted_causality_pairs

class CausalityExtraction():
    def __init__(self):
        pass

    def verb_noun_extraction(self, content):
        nlp = spacy.load("en_core_web_sm")
        
        for i in range(len(content)):
            cause = nlp(content[i].get("cause"))
            final_cause = ""
            final_effect = ""
            for token in cause:
                # if token.pos_ in ('PROPN', 'VERB' ,'NOUN'):
                if token.pos_ in ('VERB' ,'NOUN'):
                    if not final_cause:
                        # final_cause = token.text    
                        final_cause = token.text
                    else: 
                        final_cause += "," + token.text
                    

            effect = nlp(content[i].get("effect"))
            for token in effect:
                 if token.pos_ in ('VERB' ,'NOUN'):
                    if not final_effect:
                        final_effect = token.text
                    else: 
                        final_effect += "," + token.text

            content[i].update(cause=final_cause, effect=final_effect)
        
        return content

       
class CausalityGeneralisation():
    def __init__(self, hypernym_level=2):
        # 2 level up in inherited hypernym hierarchy, avoid too general
        self.hypernym_level = hypernym_level

    def generalisation(self, content):
        nlp = spacy.load("en_core_web_sm")
        
        for i in range(len(content)):
            cause = nlp(content[i].get("cause"))
            final_cause = ""
            final_effect = ""
            for token in cause:
                # if token.pos_ in ('PROPN', 'VERB' ,'NOUN'):
                if token.pos_ in ('NOUN'):
                    if not final_cause:
                        final_cause = self.wordnet(token.text,i)    
                    else: 
                        final_cause += "," + self.wordnet(token.text,i)
                elif token.pos_ in ('VERB'):
                    if not final_cause:
                        final_cause = self.verbnet(token.text,i)    
                    else: 
                        final_cause += "," + self.verbnet(token.text,i)
            

            effect = nlp(content[i].get("effect"))
            for token in effect:
                if token.pos_ in ('NOUN'):
                    if not final_effect:
                        final_effect = self.wordnet(token.text,i)  
                    else: 
                        final_effect += "," + self.wordnet(token.text,i)
                elif token.pos_ in ('VERB'):
                        if not final_cause:
                            final_cause = self.verbnet(token.text,i)    
                        else: 
                            final_cause += "," + self.verbnet(token.text,i)

            content[i].update(cause=final_cause, effect=final_effect)
        
        return content

    def wordnet(self, word, index):        
        syn_words = wn.synsets(word)

        if len(syn_words)==0:
            return '<empty>'

        valid_flag=0
        for syn_word in syn_words:
            if syn_word.name().split('.')[1]=='n':
                word = syn_word
                valid_flag=1
                break

            if valid_flag==0:
                print("ERROR: NO NOUN \"{}\"".format(word))
                return word

        for l in range(self.hypernym_level):
            hypernym = word.hypernyms()
            if len(hypernym) != 0 and "entity" not in hypernym[0].name().split('.')[0].split("_"):
                word = hypernym[0]
            else:
                print("Line " + str(index))
                print(hypernym)
                break

        return word.name()

    def verbnet(self, word, index):
        syn_words = wn.synsets(word) #get 'go.v.01' if verb is 'go', verbnet only takes present tense
        if len(syn_words)==0:
            print("error: no syn_word \"{}\"".format(word))
            return '<empty>'
       
        flag=0
        for syn_word in syn_words:
            syn_word = syn_word.name()
            if syn_word.split('.')[1]=='v':
                verb=syn_word.split('.')[0] #get 'go'
                flag=1
                break

        if flag==0:
            print("error: no verb 1\"{}\"".format(word))
            return word
        #print(verb)
        
        g_verbs = vn.classids(lemma=verb)  #'escape-51.1-2'

        if len(g_verbs)==0:
            print("error: no verb 2 \"{}\"".format(word))
            return verb

        return g_verbs[0]

def test():
    # content1 = "A country poses a threat to other countries because of its national defense policy and strategy, not its military power."
    # content2 = "US-Australia relations took a hit in February after US President Donald Trump criticized Australian Prime Minister Malcolm Turnbull on the phone over a refugee resettlement agreement former US president Barack Obama had made between the two countries."
    # content3 = "After Trump took office, the US has conducted three such operations."

    f = open(r'D:\\Desktop\\sent_news\\causality_connector\\because.txt',encoding="utf8")
    # f = open(r'D:\\Desktop\\sent_news\\causality_connector\\Cap_after.txt',encoding="utf8")
    # f = open(r'D:\\Desktop\\sent_news\\causality_connector\\selected.txt',encoding="utf8")
    file = f.read()

    '''Causality Mention'''
    mention = CausalityMention()
    mention_datas = mention.extract_main(file)
    # mention_datas = mention.extract_main(content1)

    # print(mention_datas)

    '''Causality Extraction'''
    extract = CausalityExtraction()
    extract_datas = extract.verb_noun_extraction(mention_datas)

    # print(extract_datas)

    ''''Causality Generalisation'''
    generalise = CausalityGeneralisation()
    generalise_datas = generalise.generalisation(extract_datas)

    df = pd.DataFrame(generalise_datas)
    df.to_csv("data.csv", sep='\t', encoding='utf-8')




    # with open('D:\\Desktop\\sent_news\\causality_connector\\data.json', 'w', encoding='utf-8') as f:
    #     json.dump(extract_datas, f, ensure_ascii=False, indent=4)


test()
