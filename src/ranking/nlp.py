import snowballstemmer


stemmer = snowballstemmer.stemmer('english');


def stemming(text_list):
     stemmed_list = []
     for text in text_list:
          stemmed_text = ' '.join(stemmer.stemWords(text.split()))
          stemmed_list.append(stemmed_text)
     return stemmed_list
