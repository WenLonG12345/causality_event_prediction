import spacy

class CausalityExtraction():
    def __init__(self):
       pass

    def verb_noun_extraction(self, content):
        nlp = spacy.load("en_core_web_sm")

        for i in range(len(content)):
            cause = nlp(content[i].get("cause"))
            final_cause = []
            final_effect = []
            for token in cause:
                if token.pos_ in ('PROPN', 'VERB' ,'NOUN') or token.text == "not":
                    final_cause.append(token.text)
                # # if token.pos_ in ('VERB' ,'NOUN'):
                #     if not final_cause:
                #         # final_cause = token.text    
                #         final_cause = token.text
                #     else:
                #         final_cause += "," + token.text
                    
            effect = nlp(content[i].get("effect"))
            for token in effect:
                if token.pos_ in ('PROPN', 'VERB' ,'NOUN') or token.text == "not":
                # if token.pos_ in ('VERB' ,'NOUN'):
                    final_effect.append(token.text)
                    # if not final_effect:
                    #     final_effect = token.text
                    # else: 
                    #     final_effect += "," + token.text

            content[i].update(cause=final_cause, effect=final_effect)
        
        return content