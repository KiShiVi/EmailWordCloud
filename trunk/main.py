from os import path

import wordsparsers as w
import datavisualizer as g

CURRENT_DIRECTORY = path.dirname(__file__)

if __name__ == "__main__":
    text = w.read_from_txt(CURRENT_DIRECTORY + r'/example.txt')
    dict_words = w.get_dict_words_count(text)

    dataVisualizer = g.DataVisualizer(graph_words_count=10, dict_words=dict_words)
    dataVisualizer.show()
    
# import sys
# import wikipedia
# from datetime import datetime
# import emailhandler as e
# import wordcloudservice as wcs
# 
# def get_wiki(query):
#     title = wikipedia.search(query)[0]
#     page = wikipedia.page(title)
#     return page.content
# 
# 
# if __name__ == "__main__":
#     query = "Россия"
#     #query = sys.argv[1]
#     text = get_wiki(query)
#     start_time = datetime.now()
#     #text = "социология социлогию социология социологии"
#     wcs.create_wordcloud(text)
# 
#     # Provide data with mail and external password from id.mail.ru/security
#     # username = "mailru.parser.test@mail.ru"
#     # ext_password = "XM6N2JycVG63j59rRv0E"
# 
#     # gmailHandler = e.EmailHandler(username, ext_password)
#     # gmailHandler.authenticate()
#     # gmailHandler.get_messages()
#     # gmailHandler.close()
# 
#     # print(datetime.now() - start_time)
