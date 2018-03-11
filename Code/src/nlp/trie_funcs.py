import marisa_trie as marisa
import pandas as pd
import numpy as np
import codecs
import pickle
import sys

import time

import nlp_setup

def autocomplete(start_word, triee=None):
    """
    Autocomplete a word by finding the most widely used n-gram starting with it.
    :param start_word: a word to autocomplete
    :param data_path: path to the word corpus
    :param triee: an optional argument in special case where a trie already exists, main purpose
    is debugging
    :return: a string with the autocompleted word
    """

    # Get an appropriate trie
    if triee is None:
        triee, popular_dict = nlp_setup.check_cache(start_word)

    # Iterate over the trie elements that start with the start_word
    # and store the top 3 most frequent words
    item = triee.items(start_word)
    if len(start_word.split(" ")) < 1:
        next_word = next_word_indicator(item, start_word)
    else:
        next_word = False
        item = list(map(lambda x: (x[0].replace(start_word.split(" ")[0] + " ", ""), x[1]), item))

    complete_word_dict = dict(item)
    top_three = []
    while len(top_three) < 3:
        if len(complete_word_dict) > 0:
            pop_word = max(complete_word_dict, key=complete_word_dict.get)
            complete_word_dict.pop(pop_word, None)
        else:
            pop_word = max(popular_dict, key=popular_dict.get)
            popular_dict.pop(pop_word, None)

        if pop_word not in top_three:
            if not next_word:
                if pop_word.split(" ")[0] not in top_three:
                    top_three.append(pop_word.split(" ")[0])
            else:
                top_three.append(pop_word)

    complete_word = top_three

    # For the case where the autocomplete predicts the next word
    results = []
    j = 0
    while j < len(complete_word) and j < 3:
        longer = complete_word[j].split(' ')
        if len(longer) > 1 and longer[-2] in start_word:
            # Ignore the first word, which was given as an input, return only the next one
            results.append(longer[-1])
        else:
            results.append(longer[0])
        j += 1

    while len(results) <= 3:
        results.append(start_word.split(' ')[0])
    return results[0], results[1], results[2]


def next_word_indicator(item, word):
    for key, value in item:
        if key.split(" ")[0] == word.strip():
            return True

    return False


if __name__ == "__main__":
    start = time.time()
    print(autocomplete("a"))
    print((time.time() - start) * 1000)
