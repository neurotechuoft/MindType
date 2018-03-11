import sys

from nlp import trie_funcs, benchmark
# import trie_funcs


def autocomplete(word: str) -> str:
    """
    Autocomplete the word/phrase.
    If it's an incomplete word, then return the most likely completion.
    If it's a complete word, return the next word that is most likely.
    :param word: (part of) a word
    :return: completed string
    """
    return trie_funcs.autocomplete(word, "./nlp/random/w2_.txt")


if __name__ == '__main__':

    # trie = load_data("/home/igor/nlp/ngrams/w2_.txt")
    # one_letter("/home/igor/nlp/ngrams/w2_.txt")
    # popular_trie("/home/igor/nlp/ngrams/w2_.txt")
    if len(sys.argv) != 2:
        print("Usage: python complete.py phrase_to_complete")
        #print(len(sys.argv))
    #print(autocomplete(sys.argv[1]))

    #print(autocomplete('i'))

    # Benchmarks
    # Time
    #t = benchmark.benchmark('./random/test_data_w2')
    #print(t)
    # Performance
    #a,b = benchmark.performance_test()
    #print(a,b)

    # This is the result
    a1, a2, a3 = autocomplete(sys.argv[1])
    # print(a1, a2, a3)


