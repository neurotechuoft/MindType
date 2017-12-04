import trie_funcs
import sys


def compl(complete: str) -> str:
    """
    Autocomplete the word/phrase.
    If it's an incomplete word, then return the most likely completion.
    If it's a complete word, return the next word that is most likely.
    :param complete: (part of) a word
    :return: completed string
    """
    return trie_funcs.autocomplete(complete, "w2_.txt")


if __name__ == '__main__':

    # trie = load_data("/home/igor/nlp/ngrams/w2_.txt")
    # one_letter("/home/igor/nlp/ngrams/w2_.txt")
    # popular_trie("/home/igor/nlp/ngrams/w2_.txt")
    if len(sys.argv) != 2:
        print("Usage: python complete.py phrase_to_complete")
    print(compl(sys.argv[1]))

