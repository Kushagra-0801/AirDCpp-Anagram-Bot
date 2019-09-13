"""
Helper functions for help with the extension.
    1 > make_dict(word_list: str): Make the word_dict.pickle file.
        Wordlist used can be changed by changing the value of the variable WORD_LIST.
    2 > get_anagram_hub_id(api_url: str, auth_header: dict) -> int:
        Return the seesion_id for anagram game hub.
    3 > run_as_main: Call make_dict
"""

from collections import namedtuple, Counter
import pickle
import requests

WORD_LIST = "wordlist.txt"

LetterFreq = namedtuple(
    "LetterFreq", "a b c d e f g h i j k l m n o p q r s t u v w x y z"
)

BASE_DICT = {
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


def get_anagram_hub_id(api_url: str, auth_header: dict) -> int:
    """Return the seesion_id for anagram game hub."""
    hubs = requests.get(f"http://{api_url}hubs", headers=auth_header).json()
    for hub in hubs:
        if hub["identity"]["name"] == "Anagram Game Hub":
            return hub["id"]


def make_dict(word_list: str) -> None:
    """
    Open word_list and create/overwite word_dict.pickle with the contents of processed list.
    """
    word_dict = {}
    with open(word_dict) as f:
        for word in f:
            word = word.strip()
            word_hash = Counter(word)
            word_hash.update(BASE_DICT)
            word_hash = LetterFreq(**word_hash)
            try:
                word_dict[word_hash].append(word)
            except KeyError:
                word_dict[word_hash] = [word]

    with open("word_dict.pickle", "bw+") as f:
        pickle.dump(word_dict, f)


if __name__ == "__main__":
    make_dict(WORD_LIST)
