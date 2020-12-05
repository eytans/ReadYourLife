
__author__ = 'eytan'

import pickle
import sys


def save_pickle(titles_path = 'titles.txt', out_path = "titles.p"):
    f = open(titles_path, 'r', encoding='utf8')
    line = f.readline()
    d = {}
    while line:
        line_a = line.split('-')
        if len(line_a) > 3:
            line_a = ["-".join(line_a[:-2])]+line_a[-2:]
        try:
            d[line_a[0].strip()] = (int(line_a[1].strip()), int(line_a[2].strip().replace('\n', '')))
        except ValueError:
            print(line_a)
            exit(1)
        line = f.readline()
    pickle.dump(d, open(out_path, "wb"))
    return d


def load_pickle(titles_p_path="titles.p"):
    return pickle.load(open(titles_p_path, 'rb'))


def main():
    titles_path = 'titles.txt'
    out_path = "titles.p"
    if len(sys.argv) > 1:
        titles_path = sys.argv[1]
    if len(sys.argv) > 2:
        out_path = sys.argv[2]
    save_pickle(titles_path, out_path)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        print("usage: python pickle_for_titles.py save [titles_path] [out_path]")
        exit(0)
    main()
