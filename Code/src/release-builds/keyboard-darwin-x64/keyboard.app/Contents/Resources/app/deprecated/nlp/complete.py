import sys

from nlp import trie_funcs, benchmark

# Use this import for testing
# import trie_funcs


def autocomplete(word: str) -> str:
    """
    Autocomplete the word/phrase.
    If it's an incomplete word, then return the most likely completion.
    If it's a complete word, return the next word that is most likely.
    :param word: (part of) a word
    :return: completed string
    """
    return trie_funcs.autocomplete(word)


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print("Usage: python complete.py phrase_to_complete")


    # Benchmarks
    # Time
    #t = benchmark.benchmark('./random/test_data_w2')
    #print(t)
    # Performance
    #a,b = benchmark.performance_test()
    #print(a,b)

    # This is the result
    a1, a2, a3 = autocomplete(sys.argv[1])
    print(a1, a2, a3)


