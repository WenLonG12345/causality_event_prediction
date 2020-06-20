import spacy
import re

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
    
    '''<effect> due to <cause>'''
    def ruler4(self, sentence):
        pattern = re.compile(r'(.*)\s(due to)\s(.*)')
        result = pattern.findall(sentence)
        data = dict()
        if result:
            data['cause'] = result[0][2]
            data['effect'] = result[0][0]
        
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
            elif self.ruler4(sentence):
                result = self.ruler4(sentence)
            else: continue

            final_result.append(result)
         
                
        return final_result

    def extract_main(self,content):
        # sanitise article
        sentences = self.sentence_segmentation(content)

        extracted_pairs = self.extract_causalit_pair(sentences)
        print('Total sentences: ' + str(len(extracted_pairs)))

        return extracted_pairs