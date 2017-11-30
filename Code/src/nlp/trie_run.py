import trie_funcs
import sys
import time


def external_run(complete: str) -> float:
    start = time.time()
    trie_funcs.autocomplete(complete, "/home/igor/nlp/ngrams/w2_.txt")
    return (time.time() - start) * 1000.0


if __name__ == '__main__':
    # trie = load_data("/home/igor/nlp/ngrams/w2_.txt")
    # one_letter("/home/igor/nlp/ngrams/w2_.txt")
    # popular_trie("/home/igor/nlp/ngrams/w2_.txt")
    if len(sys.argv) != 2:
        print("Usage python trie_run.py phrase_to_complete")
    start = time.time()

    print(trie_funcs.autocomplete(sys.argv[1], "/home/igor/nlp/ngrams/w3_.txt"))
    print((time.time() - start) * 1000.0)
