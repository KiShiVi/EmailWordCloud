from os import path

import wordsparsers as w
import datavisualizer as g

CURRENT_DIRECTORY = path.dirname(__file__)

if __name__ == "__main__":
    text = w.read_from_txt(CURRENT_DIRECTORY + r'/example.txt')
    dict_words = w.get_dict_words_count(text)

    dataVisualizer = g.DataVisualizer(graph_words_count=3, dict_words=dict_words)
    dataVisualizer.show()

