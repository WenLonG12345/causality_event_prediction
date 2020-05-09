import pandas as pd
from pyvis.network import Network

class CausalityNetwork():
    def __init__(self):
       pass

    def network(self, file):
        net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")
        net.barnes_hut()
        data = pd.read_csv(file, sep="\t")

        cause = data["cause"]
        effect = data["effect"]

        edge_data = zip(cause,effect)

        for e in edge_data:
            cause_data = str(e[0])
            effect_data = str(e[1])

            net.add_node(cause_data, cause_data, title=cause_data)
            net.add_node(effect_data, effect_data, title=effect_data)
            net.add_edge(cause_data, effect_data)
        
        # neighbour_map = net.get_adj_list()

        # for node in net.nodes:
        #     node['title'] += " Neighbours: <br>" + "<br>".join(neighbour_map[node["id"]])
        #     node["value"] = len(neighbour_map[node["id"]])

        net.show("causality_network.html")