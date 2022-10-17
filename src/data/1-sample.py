import argparse
import random


def reservoir_sampling(l, k):
    it = iter(l)
    try:
        result = [next(it) for _ in range(k)]
    except StopIteration:
        raise ValueError("Sample larger than population")

    for i, item in enumerate(it, start=k):
        s = random.randint(0, i)
        if s < k:
            result[s] = item

    random.shuffle(result)
    return result


def sample(file_path, n_lines):
    with open(file_path) as infile, open(
        file_path + '.' + str(n_lines), 'w') as outfile:
        for line in reservoir_sampling(infile, n_lines):
            outfile.write(line)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sample pubmed file')
    parser.add_argument("--file_path", type=str, required=True)
    parser.add_argument("--n_lines", type=int, help="Numer of lines to sample", required=True)
    sample(parser.parse_args().file_path, parser.parse_args().n_lines)