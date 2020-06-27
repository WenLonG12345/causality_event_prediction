import pke

class KeywordExtraction():
    def __init__(self):
        pass

    def extract(self, sentence):
        # initialize keyphrase extraction model, here TopicRank
        extractor = pke.unsupervised.TopicRank()

        # sentence = "the Philippines won the arbitration case against China over the disputed South China Sea."
        # sentence = "Philippine Rodrigo Duterte called for a cabinet meeting"

        # load the content of the document, here document is expected to be in raw
        # format (i.e. a simple text file) and preprocessing is carried out using spacy
        extractor.load_document(input=sentence, language='en')

        # keyphrase candidate selection, in the case of TopicRank: sequences of nouns
        # and adjectives (i.e. `(Noun|Adj)*`)
        extractor.candidate_selection()

        # candidate weighting, in the case of TopicRank: using a random walk algorithm
        extractor.candidate_weighting()

        # N-best selection, keyphrases contains the 10 highest scored candidates as
        # (keyphrase, score) tuples
        keyphrases = extractor.get_n_best(n=1)

        return keyphrases[0][0]

    def main(self, content):
        for i in range(len(content)):
            cause = content[i].get("cause")
            effect = content[i].get("effect")
        
            keyphrased_cause = self.extract(cause)
            keyphrased_effect = self.extract(effect)

            content[i].update(cause=keyphrased_cause, effect=keyphrased_effect)
        
        return content

        
