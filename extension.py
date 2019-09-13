import argparse
from collections import Counter
import pickle
import requests
from helpers import LetterFreq, BASE_DICT, get_anagram_hub_id, get_questions

parser = argparse.ArgumentParser()
parser.add_argument("--name", help="Extension name", dest="name")
parser.add_argument("--apiUrl", help="API URL", dest="api_url")
parser.add_argument("--authToken", help="API session token", dest="auth_token")
parser.add_argument("--settingsPath", help="Setting directory", dest="settings_path")
parser.add_argument("--logPath", help="Log directory", dest="log_path")
parser.add_argument(
    "--debug", help="Enable debug mode", dest="debug", action="store_true"
)
parser.set_defaults(debug=False)


WORD_DICT = pickle.load("word_dict.pickle")


if __name__ == "__main__":
    args = parser.parse_args()
    auth_header = {"Authorization": args.auth_token}
    hub_id = get_anagram_hub_id(args.api_url, auth_header)
    for question in get_questions(args.api_url, auth_header, hub_id):
        word = Counter(question)
        word.update(BASE_DICT)
        word = LetterFreq(**word)
        possible_answers = WORD_DICT[word]
        for answer in possible_answers:
            requests.post(
                f"http://{args.api_url}hubs/{hub_id}/chat_message",
                json={"text": answer},
                headers=auth_header,
            )
