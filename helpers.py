"""
Helper functions for help with the extension.
    1 > make_dict(word_list: str): Make the word_dict.pickle file.
        Wordlist used can be changed by changing the value of the variable WORD_LIST.
    2 > get_anagram_hub_id(api_url: str, auth_header: dict) -> int:
        Return the seesion_id for anagram game hub.
    3 > get_questions(api_url: str, auth_header: dict, hub_id: int):
        Generator function that looks for messages that contain a new anagram word
        and yield them without spaces and lowercased.
        Note: It is possible that some messages be skipped from in between.
    4 > run_as_main: Call make_dict
"""

from collections import namedtuple, Counter
import pickle
import re
import requests

WORD_LIST = "wordlist.txt"


def get_anagram_hub_id(api_url: str, auth_header: dict) -> int:
    """Return the seesion_id for anagram game hub."""
    hubs = requests.get(f"http://{api_url}hubs", headers=auth_header).json()
    for hub in hubs:
        if hub["identity"]["name"] == "Anagram Game Hub":
            return hub["id"]


def get_questions(api_url: str, auth_header: dict, hub_id: int):
    """
    Generator function that looks for messages that contain a new anagram word
    and yield them without spaces and lowercased.
    Note: It is possible that some messages be skipped from in between.
    """
    QUESTION_REGEX = re.compile(r"\*\*\* New Anagram Word is \[ (?P<letters>(\w\s)+)")
    latest_message_id = 0
    while True:
        messages = requests.get(
            f"http://{api_url}hubs/{hub_id}/messages/5", headers=auth_header
        ).json()
        for message in messages:
            if "chat_message" not in message:
                continue
            if message["chat_message"]["id"] <= latest_message_id:
                continue
            latest_message_id = message["chat_message"]["id"]
            match = re.search(QUESTION_REGEX, message["chat_message"]["text"])
            if match:
                letters = match.group("letters")
                yield letters.lower().replace(" ", "")


def make_dict(word_list: str) -> None:
    """
    Open word_list and create/overwite word_dict.pickle with the contents of processed list.
    """
    word_dict = {}
    with open(word_list) as f:
        for word in f:
            word = word.strip()
            word_key = "".join(sorted(word))
            try:
                word_dict[word_key].append(word)
            except KeyError:
                word_dict[word_key] = [word]

    with open("word_dict.pickle", "bw+") as f:
        pickle.dump(word_dict, f)


if __name__ == "__main__":
    make_dict(WORD_LIST)
