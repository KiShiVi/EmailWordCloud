import sys
from os import path
import numpy as np
from PIL import Image
import wikipedia
from wordcloud import WordCloud, STOPWORDS

currdir = path.dirname(__file__)


def get_wiki(query):
    title = wikipedia.search(query)[0]
    page = wikipedia.page(title)
    return page.content


def create_wordcloud(text):
    mask = np.array(Image.open(path.join(currdir, "cloud.jpg")))

    stopwords = set(STOPWORDS)

    wc = WordCloud(background_color="white",
                   max_words=50000,
                   mask=mask,
                   stopwords=stopwords,
                   prefer_horizontal= 1,
                   width=1920,
                   height=1920
                   )

    wc.generate(text)
    wc.to_file(path.join(currdir, "output.png"))


if __name__ == "__main__":
    query = "Россия"
    #query = sys.argv[1]
    text = get_wiki(query)
    #text = "социология социлогию социология социологии"
    create_wordcloud(text)
