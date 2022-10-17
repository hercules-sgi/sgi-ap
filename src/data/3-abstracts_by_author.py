import argparse
import json
import string
import pandas as pd


def parse_line(line):
    line_dict = json.loads(line)
    authors_list = line_dict['authors']
    abstract =  ' '.join(line_dict['abstract_text'])
    abstract = abstract.translate(str.maketrans('', '', string.punctuation)).replace('\n', ' ')
    abstract = ' '.join([w for w in abstract.split() if len(w)>1])  
    return [(author, abstract) for author in authors_list]


def group_by_author(articles):
    df = pd.DataFrame(articles, columns=['Author', 'Abstract'])
    df_grouped = df.groupby(['Author'], as_index = False).agg({'Abstract': ' '.join})
    df_grouped['n_articles'] = list(df.groupby(['Author'])['Author'].count())
    return df_grouped


def generate_file(file_path):
    """Generates a dataset CSV file from a file containing a list of json artifacts .

     Parameters:
     file_path (string): Full path of json file
    """
    # Get a list of list
    lines = [parse_line(line) for line in open(file_path, 'r').readlines()]
    # Flatter the list of list
    author_abstracts = [x for xs in lines for x in xs]
    # Create CSV file: author, abstract, number of articles by author
    group_by_author(author_abstracts).to_csv('abstracts.csv', index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script to generate a grofinal author-abstracts dataset')
    parser.add_argument("--file_path", type=str, required=True)
    generate_file(parser.parse_args().file_path)

