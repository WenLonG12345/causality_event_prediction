import numpy as np
import pandas as pd
import csv
from gensim.models import KeyedVectors

class Embedding():
    def __init__(self):
        pass

    def combine_vocab(self, content, target):
        vocab = []
        for i in range(len(content)):
            t = content[i].get(target)
            vocab += t

        return vocab

    def remove_duplicated_word(self, my_list):
        return sorted(set(my_list), key=lambda x:my_list.index(x))

    def load_glove_vector(self):
        filename = 'D:\Downloads\glove.6B\glove.6B.200d.word2vec'
        word2vec_model = KeyedVectors.load_word2vec_format(filename, binary=False)

        return word2vec_model


    def main(self, content):
        cause_vocab = self.combine_vocab(content, 'cause')
        effect_vocab = self.combine_vocab(content, 'effect')

        total_vocab = cause_vocab + effect_vocab
        total_vocab = self.remove_duplicated_word(total_vocab)

        word2idx = {w: idx for (idx, w) in enumerate(total_vocab)}
        idx2word = {idx: w for (idx, w) in enumerate(total_vocab)}

        vocabulary_size = len(total_vocab)

        print("Loading glove vector....")
        model = self.load_glove_vector()

        result = model.most_similar(positive=['woman', 'king'], negative=['man'], topn=1)

        print(result)



