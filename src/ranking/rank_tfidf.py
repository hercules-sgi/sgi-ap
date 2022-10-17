from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
import nlp
import argparse
import sys


def calculate_tfidf_similarity(dataset, query):
    """Calculate cosine distance between abstracs associated to authors and a search query.

     Parameters:
     dataset (array): List of abstracts associated to an author
     query (string): Search query

     Return:
     array of indexes, 
     array of distances

    """
    tfidf_vectorizer = TfidfVectorizer(stop_words='english', lowercase=False)
    tfidf_matrix = tfidf_vectorizer.fit_transform(dataset + query)
    # Calculate cosine similarity of documents with the last one (the query)
    distance_vector = cosine_similarity(
        tfidf_matrix, 
        tfidf_matrix[-1]).flatten()[:-1].copy()
    ranked_indexes = np.flip(np.argsort(distance_vector)) 
    return ranked_indexes, distance_vector[ranked_indexes] 


def get_authors(author_abstracts_file, query):
    """Get list of authors ranked.

        Parameters:
            author_abstracts_file (array): Path of authors & abstracts file
            query (string): Search query

        Return:
            list of authors (strings)
            list of distances (float)
    """
    authors_df = pd.read_csv(author_abstracts_file, encoding="ISO-8859-15")
    abstracts = nlp.stemming(list(authors_df['Abstract']))
    query_list = nlp.stemming([query])
    author_ranking, distances = calculate_tfidf_similarity(abstracts, query_list)
    return list(authors_df.iloc[author_ranking, 0]), distances


def print_results(authors, distances, n_elements):
    results = zip(authors, distances)
    msg = repr([(x[0].encode(sys.stdout.encoding), x[1]) for x in results[0:n_elements]]).decode('string-escape')
    print(msg)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script to get a list of authors ranked')
    parser.add_argument("--file_path", type=str, required=True)
    parser.add_argument("--query", type=str, required=True)
    parser.add_argument("--n", type=int, nargs="?", const=3, default=3)
    authors, distances = get_authors(parser.parse_args().file_path, parser.parse_args().query)
    print_results(authors, distances, parser.parse_args().n)
