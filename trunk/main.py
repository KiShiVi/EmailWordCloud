import sys
from os import path
import numpy as np
from PIL import Image
import wikipedia
from wordcloud import WordCloud, STOPWORDS

from datetime import datetime
import emailhandler as e

currdir = path.dirname(__file__)

def get_wiki(query):
    title = wikipedia.search(query)[0]
    page = wikipedia.page(title)
    return page.content


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


if __name__ == "__main__":
    query = "Россия"
    #query = sys.argv[1]
    text = get_wiki(query)
    start_time = datetime.now()
    #text = "социология социлогию социология социологии"
    create_wordcloud(text)

    # Provide data with mail and external password from id.mail.ru/security
    # username = "mailru.parser.test@mail.ru"
    # ext_password = "XM6N2JycVG63j59rRv0E"

    # gmailHandler = e.EmailHandler(username, ext_password)
    # gmailHandler.authenticate()
    # gmailHandler.get_messages()
    # gmailHandler.close()

    # print(datetime.now() - start_time)

