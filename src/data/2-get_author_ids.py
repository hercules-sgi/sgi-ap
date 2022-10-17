import argparse
import json
import os
from pymed import PubMed
from nbformat import write


pubmed = PubMed(tool="PoC", email="jose.fernandez@treelogic.com")


def get_authors(article_id):    
    try:
        authors_list = []
        for article in pubmed.query(article_id, max_results=1):
            for author in article.toDict()['authors']:
                lastname = author['lastname']
                firstname = author['firstname']
                authors_list.append(firstname + ' ' + lastname)
            return authors_list
    except:
        return None


def delete_file(file_path):
    file_path = file_path + '.with_authors.txt'
    if os.path.exists(file_path):
        os.remove(file_path)


def write_file(file_path, line):
    with open(file_path + '.with_authors.txt', "a") as file_object:
        file_object.write(line)


def edit_line(line):
    try:
        article_dict = json.loads(line)
        authors = get_authors(article_dict['article_id'])
        if authors is not None:
            article_dict['authors'] = authors
            return json.dumps(article_dict) + '\n'
    except:
        return None


def generate_file(file_path):
    counter = 0
    articles_file = open(file_path, 'r')
    lines = articles_file.readlines()
    n_lines = len(lines)
    delete_file(file_path)
    for line in lines:
        new_line = edit_line(line)
        if new_line is not None:
            counter += 1
            write_file(file_path, new_line)
            print("Article {} of {}".format(counter, n_lines))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sample ')
    parser.add_argument("--file_path", type=str, required=True)
    generate_file(parser.parse_args().file_path)
