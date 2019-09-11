import argparse
import pickle
from collections import namedtuple, Counter

parser = argparse.ArgumentParser(
    prog="Word Dictionary Builder",
    description="Create a pickled dictionary containing a mapping of letter frequency to words",
    allow_abbrev=False,
)

parser.add_argument(
    "-w",
    "--wordlist",
    nargs="?",
    type=argparse.FileType("r"),
    help="Path to newline delimited wordlist",
    default="wordlist.txt",
    dest="word_list",
)

args = parser.parse_args()

LetterFreq = namedtuple(
    "LetterFreq", "a b c d e f g h i j k l m n o p q r s t u v w x y z"
)

word_dict = {}
base_dict = {
    "a": 0,
    "b": 0,
    "c": 0,
    "d": 0,
    "e": 0,
    "f": 0,
    "g": 0,
    "h": 0,
    "i": 0,
    "j": 0,
    "k": 0,
    "l": 0,
    "m": 0,
    "n": 0,
    "o": 0,
    "p": 0,
    "q": 0,
    "r": 0,
    "s": 0,
    "t": 0,
    "u": 0,
    "v": 0,
    "w": 0,
    "x": 0,
    "y": 0,
    "z": 0,
}

for word in args.word_list:
    word = word.strip()
    word_hash = Counter(word)
    word_hash.update(base_dict)
    word_hash = LetterFreq(**word_hash)
    try:
        word_dict[word_hash].append(word)
    except KeyError:
        word_dict[word_hash] = [word]

with open("word_dict.pickle", "bw+") as f:
    pickle.dump(word_dict, f)
