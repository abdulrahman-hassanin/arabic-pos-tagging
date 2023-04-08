from farasa.pos import FarasaPOSTagger 
import networkx as nx
import matplotlib.pyplot as plt
import arabic_reshaper
from bidi.algorithm import get_display
import re

class POS_Tagging:
    def __init__(self, text) -> None:
        self.text = text
        self.pos_tagged = None
        self.tags_set = set()

    def POS_Tag(self):
        """
        Extract POS Tagging
        """
        pos_tagger = FarasaPOSTagger()
        self.pos_tagged = pos_tagger.tag_segments(text, combine_subtokens=True)

        for pos in self.pos_tagged:
            for tag in pos.tags:
                self.tags_set.add(tag)

    def draw_graph(self):
        """
        Draw the POS-Tagging using NetworkX
        """
        # Create a graph
        G = nx.Graph()

        # Create tags as nodes
        for tag in self.tags_set:
            G.add_node(tag)

        # add edges to the graph
        for pos in self.pos_tagged:
            for i in range(len(pos.tokens)):
                word = pos.tokens[i]
                tag = pos.tags[i]   
                # Arabic text preprocessing 
                reshaped_word = arabic_reshaper.reshape(word)
                arword = get_display(reshaped_word)
        
                for node in G.copy().nodes():
                    if tag == node:
                        G.add_edge(tag, arword)

        # draw the graph
        plt.figure()
        pos = nx.spring_layout(G, k=0.5)
        
        color_map = []
        for node in G:
            if re.search('[a-zA-Z]', node) :
                color_map.append('darksalmon')   
            else: 
                color_map.append('steelblue')
                
        nx.draw(G, pos, node_color=color_map, with_labels=True, alpha=0.7)
        plt.title("Arabic POS-Tagging with NetworkX")  # set title

        # showing the graph
        plt.axis('off')
        plt.show()

if __name__ == '__main__':
    text = """
يُشار إلى أن اللغة العربية يتحدثها أكثر من 422 مليون نسمة ويتوزع متحدثوها في المنطقة المعروفة باسم الوطن العربي بالإضافة إلى العديد من المناطق الأخرى المجاورة مثل الأهواز وتركيا وتشاد والسنغال وإريتريا وغيرها. وهي اللغة الرابعة من لغات منظمة الأمم المتحدة الرسمية الست.
    """

    pos_tagger = POS_Tagging(text)
    pos_tagger.POS_Tag()
    pos_tagger.draw_graph()