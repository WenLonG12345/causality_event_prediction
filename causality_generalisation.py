import spacy
from nltk.corpus import wordnet as wn
from nltk.corpus import verbnet as vn


class CausalityGeneralisation():
    def __init__(self, hypernym_level=1):
        # 2 level up in inherited hypernym hierarchy, avoid too general
        self.hypernym_level = hypernym_level

    def lemma(self, content, nlp):
        for i in range(len(content)):
            cause = nlp(content[i].get("cause"))
            effect = nlp(content[i].get("effect"))
            lemma_cause = ""
            lemma_effect = ""
            for token in cause:
                lemma_cause += token.lemma_

            for token in effect:
                lemma_effect += token.lemma_

            content[i].update(cause=lemma_cause, effect=lemma_effect)
        
        return content
        

    def generalisation(self, content):
        nlp = spacy.load("en_core_web_sm")
        
        content = self.lemma(content, nlp)

        for i in range(len(content)):
            cause = nlp(content[i].get("cause"))
            final_cause = ""
            final_effect = ""
            for token in cause:
                if token.pos_ in ('NOUN','PROPN'):
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
                if token.pos_ in ('NOUN','PROPN'):
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
            return word

        valid_flag=0
        for syn_word in syn_words:
            if syn_word.name().split('.')[1]=='n':    #take note not only 'n'
                word = syn_word
                valid_flag=1
                break

            if valid_flag==0:
                print("error: no noun \"{}\"".format(word))
                return word

        for l in range(self.hypernym_level):
            hypernym = word.hypernyms()
            if len(hypernym) != 0 and "entity" not in hypernym[0].name().split('.')[0].split("_"):
                word = hypernym[0]
            else:
                print("error: no hypernym - " + word.name())
                break

        return (word.name()).split('.')[0]

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
