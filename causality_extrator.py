import re
import spacy
import json

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
                if token.pos_ in ('PROPN', 'VERB' ,'NOUN'):
                    if not final_cause:
                        final_cause = token.text    
                    else: 
                        final_cause += "," + token.text
            

            effect = nlp(content[i].get("effect"))
            for token in effect:
                 if token.pos_ in ('PROPN', 'VERB' ,'NOUN'):
                    if not final_effect:
                        final_effect = token.text    
                    else: 
                        final_effect += "," + token.text

            content[i].update(cause=final_cause, effect= final_effect)
        
        return content



def test():
    # content1 = "The tension in the South China Sea is not because of the implementation of international law but because international law has not been fully respected."
    # content2 = "US-Australia relations took a hit in February after US President Donald Trump criticized Australian Prime Minister Malcolm Turnbull on the phone over a refugee resettlement agreement former US president Barack Obama had made between the two countries."
    # content3 = "After Trump took office, the US has conducted three such operations."

    # f = open(r'D:\\Desktop\\sent_news\\causality_connector\\because.txt',encoding="utf8")
    # f = open(r'D:\\Desktop\\sent_news\\causality_connector\\Cap_after.txt',encoding="utf8")
    f = open(r'D:\\Desktop\\sent_news\\causality_connector\\selected.txt',encoding="utf8")
    file = f.read()

    '''Causality Mention'''
    mention = CausalityMention()
    mention_datas = mention.extract_main(file)
    # mention_datas = mention.extract_main(content3)

    # print(mention_datas)

    '''Causality Extraction'''
    extract = CausalityExtraction()
    extract_datas = extract.verb_noun_extraction(mention_datas)

    # print(extract_datas)
    with open('D:\\Desktop\\sent_news\\causality_connector\\data.json', 'w', encoding='utf-8') as f:
        json.dump(extract_datas, f, ensure_ascii=False, indent=4)


test()
