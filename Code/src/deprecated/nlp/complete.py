import sys
from socketIO_client import SocketIO
import trie_funcs

test_port = 8001

def autocomplete(word: str) -> str:
    """
    Autocomplete the word/phrase.
    If it's an incomplete word, then return the most likely completion.
    If it's a complete word, return the next word that is most likely.
    :param word: (part of) a word
    :return: completed string
    """
    return trie_funcs.autocomplete(word)

# The code below is to simulate requests from the client
def process_predictions(*args):
    print("predictions: ", args)


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print("Usage: python complete.py phrase_to_complete")
        exit(1)

    socket_client = SocketIO("localhost", test_port)
    socket_client.connect()
    socket_client.emit("predict", sys.argv[1], process_predictions)
    socket_client.wait_for_callbacks(seconds=1)
