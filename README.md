# Project organization

```
├── README.md          <- The top-level README for developers using this project.
│
├── data
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default Sphinx project; see sphinx-doc.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.py           <- Make this project pip installable with `pip install -e`
└── src                <- Source code for use in this project.
    ├── __init__.py    <- Makes src a Python module
    │
    ├─── data                            <- Data-related scripts
    |    ├── 1-sample.py                 <- Script to sample lines from a large dataset
    |    ├── 2-get_author_ids.py         <- Script to get author IDs by connecting to pubmed API
    |    └── 3-abstracts_by_author.py    <- Script to generate CSV file with:   
    |      								           - One line per article
    |                                       - Headers: author, abstract (text without punctuation), n_articles
    |
    └─── ranking                    <- Scripts to rank researches
         ├── nlp.py                 <- Module with functions to apply NLP transformations:
         |       					         - Tokenization
         |   						         - Stemming
         ├── rank_tfidf.py          <- Get authors and cosine distances using tf-idf vectors
         └── rank_doc2vec.py        <- Get authors and cosine distances using doc2vec vectors 

```
# Links

- Confuence: https://confluence.treelogic.com/pages/viewpage.action?pageId=87819771
- Doc2Vec: https://github.com/jhlau/doc2vec
- Dataset: https://huggingface.co/datasets/ccdv/pubmed-summarization/resolve/main/train.zip


# Data

## 1. Raw Data 

Since a viable dataset is not available at the current stages of the project, it has been decided to use an open dataset with a similar structure to the one that will be available in the system:

- Download from here:  https://huggingface.co/datasets/ccdv/pubmed-summarization/resolve/main/train.zip
- More info.: https://www.tensorflow.org/datasets/catalog/scientific_papers?hl=en#scientific_paperspubmed

This file is in jsonline format where each line is a json object corresponding to one scientific paper from PubMed, with the following structure:
```
{ 
  'article_id': str,
  'abstract_text': List[str],
  'article_text': List[str],
  'section_names': List[str],
  'sections': List[List[str]]
}
```

## 2. Data preparation

In order to create a valid dataset:

1. Download the raw data file: https://huggingface.co/datasets/ccdv/pubmed-summarization/resolve/main/train.zip
2. Unzip file
3. From parent folder, run 1-sample.py script:
   ```
   python ./src/data/1-sample.py --file_path ./data/raw/train.txt --n_lines 20000
   ```
4. Run 2-get_author_ids.py  (note: python3 required)
   ```
   python ./src/data/2-get_author_ids.py --file_path ./data/raw/train.txt.20000 
   ```
5.  Run 3-abstracts_by_author.py 
   ```
   python ./src/data/3-abstracts_by_author.py --file_path ./data/raw/train.txt.20000.with_authors.txt
   ```

It will create a file named ./data/raw/abstracts.csv

## 3. Processed Data

As described, the data preparation phase will yield a CSV file named "abstracts.csv". Headers:
- Authors: list of authors names
- Abstract: list of string of abstract keywords
- n_articles: number of articles for the given author from which abstracts keywords have been extracted


# Installation

The project requires Python 2.7 in order to load Doc2Vec Gensim language models.

0. Requirements:
- Conda: 

1. Installation steps:
```
conda create -n python2 python=2.7 anaconda
```

2. Activate environment:
```
source activate python2
```

3. Clone project:
```
git clone http://gitlab.treelogic.local/operaciones/hercules/sgi/sgi-ap
```

4. Install dependencies:
```
cd <LOCAL_PATH>/sgi-ap
pip install requirements.txt
```
Please note: change your <LOCAL_PATH> to fit your local folder.

# Usage

Please note: python2 required.

From project parent folder:

TF-IDF
```
$ python ./src/ranking/rank_tfidf.py --file_path ./data/processed/abstracts_54-authors.csv --query "<YOUR_SEARCH_QUERY>"
```

Doc2Vec
```
$ python ./src/ranking/rank_doc2vec.py --file_path ./data/processed/abstracts_54-authors.csv --query "<YOUR_SEARCH_QUERY>"
```
