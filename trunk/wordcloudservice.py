import numpy as np
from PIL import Image
from wordcloud import WordCloud, STOPWORDS
from os import path

currdir = path.dirname(__file__)

def create_wordcloud(text):
    mask = np.array(Image.open(path.join(currdir, r"resources/cloud.jpg")))

    stopwords = set(STOPWORDS)

    wc = WordCloud(background_color="white",
                   max_words=500,
                   mask=mask,
                   stopwords=stopwords,
                   prefer_horizontal= 1,
                   width=1920,
                   height=1080,
                   scale=1
                   )

    wc.generate(text)
    wc.to_file(path.join(currdir, r"output/output.png"))