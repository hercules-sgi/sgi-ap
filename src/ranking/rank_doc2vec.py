import gensim
import argparse
import pandas as pd
import numpy as np
import sys
from sklearn.metrics.pairwise import cosine_similarity


#parameters
model_path = "./models/doc2vec.bin"
start_alpha=0.01
infer_epoch=1000

#load model
model = gensim.models.Doc2Vec.load(model_path)


def get_vector_list(doc_list):
    """
    Returns a list of vectors.

        Parameters:
            doc_list (array of strings): A list of strings (documents

        Returns:
            vectors (array): List of lists of float numbers
    """
    vectors = []
    for doc in doc_list:
        vector = model.infer_vector(doc.split(), alpha=start_alpha, steps=infer_epoch)
        vectors.append(vector)
    return vectors


def calculate_doc2vec_similarity(dataset, query):
    """Calculate cosine distance between abstracs associated to authors and a search query.

        Parameters:
            dataset (array of strings): List of abstracts associated to an author
            query (string): Search query

        Return:
            array of indexes, array of distances
    """
    dataset_vectors = get_vector_list(dataset)
    query_vector = get_vector_list([query])
    distance_vector = cosine_similarity(
        dataset_vectors,  query_vector).flatten().copy()
    ranked_indexes = np.flip(np.argsort(distance_vector)) 
    return ranked_indexes, distance_vector[ranked_indexes]  


def get_authors(author_abstracts_file, query):
    """Get list of authors ranked.

        Parameters:
            author_abstracts_file (array): Path of authors & abstracts file
            query (string): Search query

        Return:
            list of strings
    """    
    authors_df = pd.read_csv(author_abstracts_file)
    abstracts = list(authors_df['Abstract'])
    author_ranking, distances = calculate_doc2vec_similarity(abstracts, query)
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
