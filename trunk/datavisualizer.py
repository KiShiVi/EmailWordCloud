import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import multidict as multidict
import numpy as np

from PIL import Image
from wordcloud import WordCloud, STOPWORDS
from os import path

import wordsparsers
import loggingTime

CURRENT_DIRECTORY = path.dirname(__file__)
MAX_GRAPHIC_WORDS = 50


# Singleton big-drawer class (cloud and graphic)
class DataVisualizer(object):
    instance = None

    def __new__(cls, dict_words: multidict, graph_words_count: int = 10):
        if cls.instance is None:
            cls.instance = super(DataVisualizer, cls).__new__(cls)
            cls._graph_words_count = graph_words_count
            cls._dict_words = dict_words
            cls._logger = loggingTime.LogTime()
        return cls.instance

    # dict_words<string, int> must be already 'sorted'.
    def __init__(self, dict_words: multidict, graph_words_count: int = 10):
        assert graph_words_count >= 0 or graph_words_count <= MAX_GRAPHIC_WORDS, \
                'Используйте адекватное кол-во слов для графика'

        self._graph_words_count = graph_words_count
        self._dict_words = dict_words
        self._logger = loggingTime.LogTime()

    def set_dict_words(self, dict_words: multidict) -> None:
        self._dict_words = dict_words

    # Please, use narrowing change, otherwise update the dict_words.
    def set_graph_words_count(self, graph_words_count: int) -> None:
        assert graph_words_count >= 0 or graph_words_count <= MAX_GRAPHIC_WORDS, \
                'Используйте адекватное кол-во слов для графика'
        self._graph_words_count = graph_words_count

    def _create_graphic(self) -> None:
        assert self._dict_words is not None, 'Словарь отсутствует, либо сломан после обновления размера'

        # hard-coded "sorting" and slicing of dictionary.
        dict_top_words = wordsparsers.get_sorted_dictionary(self._dict_words, self._graph_words_count)

        fig, ax = plt.subplots()
        # set margins for long words
        plt.subplots_adjust(left=0.3, bottom=0.1, right=0.9, top=0.9, wspace=0, hspace=0)

        # error = np.random.rand(len(words))
        # We can show the error of word calculation = ~20%.
        error = None
        y_pos = np.arange(self._graph_words_count)
        sorted_values = sorted(dict_top_words.values(), reverse=True)

        ax.barh(y_pos, width=sorted_values, height=0.9, xerr=error, align='center')
        ax.set_yticks(y_pos, labels=dict_top_words.keys())
        ax.invert_yaxis()  # labels read top-to-bottom
        ax.set_xlabel('Количество слов')
        ax.set_title('Самые частые слова:')

        # show only valuable x-Axis and y-Axis ticks.
        plt.xticks(list(dict_top_words.values()))

    def _create_cloud(self) -> dict:
        mask = np.array(Image.open(path.join(CURRENT_DIRECTORY, r"resources/cloud.jpg")))
        wc = WordCloud(background_color="white",
                       max_words=50000,
                       mask=mask,
                       # stopwords=stopwords,  # we use our own stopwords.
                       prefer_horizontal=1,
                       width=1920,
                       height=1080,
                       scale=1
                       )

        # optimized version with our multidict<string, int>
        wc.generate_from_frequencies(self._dict_words)
        wc.to_file(path.join(CURRENT_DIRECTORY, r"output/output.png"))

        plt.figure("Облако слов")
        img = mpimg.imread(path.join(CURRENT_DIRECTORY, r"output/output.png"))

        plt.imshow(img)
        plt.axis('off')
        plt.show()

        # dict<string, float> frequencies if you need
        return wc.words_

    def show(self) -> None:
        # graphic creating
        self._logger.start()
        self._create_graphic()
        self._logger.stop("Graphic has calculated")
        # set window's title
        plt.get_current_fig_manager().set_window_title('График частых слов')
        # don't block the main-thread (for 2nd window showing)
        plt.draw()

        # cloud creating
        self._logger.start()
        self._create_cloud()
        self._logger.stop("Cloud has created")
        plt.show()
