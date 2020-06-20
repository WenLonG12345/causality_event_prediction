import causality_mention
import causality_extraction
import causality_generalisation

import spacy
import json
import pandas as pd
import numpy as np
import itertools
import math
    
class Embedding():
    def __init__(self):
        pass

    
    def sigmoid(self, matrix):
        return np.exp(matrix) / (1 + np.exp(matrix))


    def word2vec(self, content):
        nlp = spacy.load("en_core_web_md")
        
        for i in range(len(content)):
            print(content)
            cause = nlp(content[i].get("cause"))
            effect = nlp(content[i].get("effect"))
            final_cause = []
            final_effect = []

            for c in cause:
                if c.has_vector and not c.is_oov:
                    final_cause.append(c.vector_norm)               
                
            for e in effect:
                if e.has_vector and not e.is_oov:
                    final_effect.append(e.vector_norm)

            cause_arr = np.array([final_cause]).transpose()
            effect_arr = np.array([final_effect]).transpose()

            # print(np.shape(cause_arr))


            print("Cause:" + str(cause_arr))
            print("Effect: " + str(effect_arr))

            inner = np.inner(cause_arr, effect_arr)
            print(inner)
            print(inner.max())

            sig = self.sigmoid(inner)
            print(sig)

            # print("Cause:\n" + str(final_cause))
            # print("Effect:\n" + str(final_effect))
            # c = list(itertools.product(final_cause,final_effect))

            # print(c)


def test():
    # content1 = "Food was delicious because the dish was cooked by chef Gordon"
    content5 = "The airplane in USA exploded because of the flaw in a seal"
    # content1 = "A country poses a threat to other countries because of its national defense policy and strategy, not its military power."
    # content3 = "After Trump took office, the US has conducted three such operations."
    content1 = "A country poses a threat to other countries because of its national defense policy and strategy."

    # f = open(r'D:\\Desktop\\sent_news\\causality_connector\\segmented_sentence.txt',encoding="utf8")
    # file = f.read()

    '''Causality Mention'''
    mention = causality_mention.CausalityMention()
    # mention_datas = mention.extract_main(file)
    mention_datas = mention.extract_main(content1)

    # print(mention_datas)

    '''Causality Extraction'''
    extract = causality_extraction.CausalityExtraction()
    extract_datas = extract.verb_noun_extraction(mention_datas)

    # df = pd.DataFrame(extract_datas)
    # df.to_csv("extracted_data_1.csv", sep='\t', encoding='utf-8')

    '''word2vec'''
    word2vec = Embedding()
    word2vec_datas = word2vec.word2vec(extract_datas)

test()



