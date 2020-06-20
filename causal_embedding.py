import collections


class Embedding():
    def __init__(self):
        pass

    def combine_vocab(self, content, target):
        vocab = []
        for i in range(len(content)):
            t = content[i].get(target)
            vocab += t

        return vocab


    def word2idx(self, tokenised_content):
        word_counter = collections.Counter()
        for term in tokenised_content:
            word_counter.update({term: 1})
        
        vocab = word_counter.most_common(200)

        return vocab
    
    def main(self, content):
        cause_vocab = self.combine_vocab(content, 'cause')

        cause_vocab = self.word2idx(cause_vocab)

        print(cause_vocab)