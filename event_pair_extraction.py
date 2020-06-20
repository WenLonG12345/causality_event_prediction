import spacy

class EventPairExtraction():   
    def __init__(self):
        pass

    def extract(self, content):
        RELATED = ["nsubj","nsubjpass","amod","dobj","advmod","nmod","pobj","xcomp","compound","neg","obj"]
        ROOT = ["ROOT"]
        nlp = spacy.load("en_core_web_lg")
        for i in range(len(content)):
            cause = nlp(content[i].get("cause"))
            effect = nlp(content[i].get("effect"))
            f_cause = []
            f_effect = []
            f_cause_head = "" 
            f_effect_head = ""

            # remove stopword
            cause = nlp(self.remove_stopword(cause))
            effect = nlp(self.remove_stopword(effect))

            # CAUSE PHRASE
            # find root word
            for tok in cause:
                if (tok.dep_ in ROOT):
                    f_cause_head = tok.text
                else: continue

            # add all related word in tuple
            for tok in cause:
                if ((tok.dep_ in RELATED and str(tok.head) == f_cause_head) or tok.text == f_cause_head):
                    f_cause.append(tok.text)


            # EFFECT PHRASE
            for tok in effect:
                if (tok.dep_ in ROOT):
                    f_effect_head = tok.text
                else: continue

            for tok in effect:
                if ((tok.dep_ in RELATED and str(tok.head) == f_effect_head) or tok.text == f_effect_head):
                    f_effect.append(tok.text)

            content[i].update(cause=f_cause, effect=f_effect)
        
        return content

    def remove_stopword(self,nlp_content):
        new_sent = ""
        for tok in nlp_content:
            if not tok.is_stop or tok.text == "not":
                new_sent += tok.text + " "

        return new_sent.lower()