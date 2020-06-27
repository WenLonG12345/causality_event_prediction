import spacy

class CausalityExtraction():
    def __init__(self):
       pass

    def verb_noun_extraction(self, content):
        nlp = spacy.load("en_core_web_sm")

        for i in range(len(content)):
            cause = nlp(content[i].get("cause"))
            # final_cause = []
            # final_effect = []
            final_cause = ""
            final_effect = ""
            for token in cause:
                if token.pos_ in ('VERB' ,'NOUN') or token.text == "not":
                    # final_cause.append((token.text).lower())
                    final_cause += (token.text).lower() + " "
                    
            effect = nlp(content[i].get("effect"))
            for token in effect:
                if token.pos_ in ('VERB' ,'NOUN') or token.text == "not":
                # if token.pos_ in ('VERB' ,'NOUN'):
                    # final_effect.append((token.text).lower())
                    final_effect += (token.text).lower() + " "

            content[i].update(cause=final_cause, effect=final_effect)
        
        return content