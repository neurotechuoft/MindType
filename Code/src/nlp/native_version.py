import codecs
import pandas as pd
import pytrie
import pickle


def load_data_native(path_to_data):
    with codecs.open(path_to_data, "r", encoding='utf-8', errors='ignore') as fdata:
        grams = pd.read_table(fdata, names=["freq", "first", "second"])

    grams['freq'] = grams['freq'].apply(lambda x: (x,))
    freqs = grams['freq'].values
    phrases = grams['first'] + " " + grams['second']
    res = dict(zip(phrases, freqs))
    pytrie1 = pytrie.StringTrie(res)
    with open('pytrie.pkl', 'wb') as output:
        pickle.dump(pytrie1, output, pickle.HIGHEST_PROTOCOL)
    return pytrie1


def otherAuto(trie1, word):
    maxi = 0
    compl = ''
    for item in trie1.items(prefix = word):
        if item[1] > maxi:
            maxi = item[1]
            compl = item[0]
    if compl == '':
        return "Couldn't find autocomplete for \"{}\"".format(word)
    longer = compl.split(' ')
    if len(longer) > 1 and longer[-2] in word:
        return longer[-1]
    return longer[0]
