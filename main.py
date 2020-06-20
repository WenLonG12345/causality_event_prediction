import causality_mention
import causality_extraction
import causality_generalisation

import spacy
import json
import pandas as pd
    

def test():
    # content1 = "Food was delicious because the dish was cooked by chef Gordon"
    # content1 = "A country poses a threat to other countries because of its national defense policy and strategy, not its military power."
    # content2 = "US-Australia relations took a hit in February after US President Donald Trump criticized Australian Prime Minister Malcolm Turnbull on the phone over a refugee resettlement agreement former US president Barack Obama had made between the two countries."
    # content3 = "After Trump took office, the US has conducted three such operations."

    f = open(r'D:\\Desktop\\sent_news\\causality_connector\\data\\selected_causality_news.txt',encoding="utf8")
    file = f.read()

    '''Causality Mention'''
    mention = causality_mention.CausalityMention()
    mention_datas = mention.extract_main(file)
    # mention_datas = mention.extract_main(content1)

    df = pd.DataFrame(mention_datas)
    df.to_csv("output\\MentionDatas.csv", sep='\t', encoding='utf-8')

    '''Causality Extraction'''
    extract = causality_extraction.CausalityExtraction()
    extract_datas = extract.verb_noun_extraction(mention_datas)

    df = pd.DataFrame(extract_datas)
    df.to_csv("output\\VerbNounExtraction.csv", sep='\t', encoding='utf-8')


test()

    # causal_network = causality_network.CausalityNetwork()
    # causal_network.network("extracted_data.csv")

    # ''''Causality Generalisation'''
    # generalise = causality_generalisation.CausalityGeneralisation()
    # generalise_datas = generalise.generalisation(extract_datas)

    # df = pd.DataFrame(generalise_datas)
    # df.to_csv("generalise_data.csv", sep='\t', encoding='utf-8')

    # causal_network = CausalityNetwork()
    # causal_network.network("generalise_data.csv")