import trie_funcs
import sys
import time


def compl(complete: str) -> float:
    """
    Autocomplete the word/phrase.
    If it's an incomplete word, then return the most likely completion.
    If it's a complete word, return the next word that is most likely.
    :param complete: (part of) a word
    :return: completed string
    """
    start = time.time()
    trie_funcs.autocomplete(complete, "/home/igor/nlp/ngrams/w2_.txt")
    return (time.time() - start) * 1000.0


if __name__ == '__main__':

    # trie = load_data("/home/igor/nlp/ngrams/w2_.txt")
    # one_letter("/home/igor/nlp/ngrams/w2_.txt")
    # popular_trie("/home/igor/nlp/ngrams/w2_.txt")
    if len(sys.argv) != 2:
        print("Usage: python complete.py phrase_to_complete")
    start = time.time()

    print(trie_funcs.autocomplete(sys.argv[1], "w2_.txt"))
    print((time.time() - start) * 1000.0)
