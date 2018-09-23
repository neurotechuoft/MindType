import codecs
import json
import pickle
import numpy as np
import marisa_trie as marisa
import pandas as pd
import time

resources_path = "./resources/"

# words_dictionary from https://github.com/dwyl/english-words, using Unlisence
def load_words(check_grammar = True):
	with codecs.open("./resources/w2.txt", "r", encoding='utf-8', errors='ignore') as fdata:
		grams = pd.read_table(fdata, names=["freq", "first", "second"])
	if check_grammar:
		word_dict_path = resources_path + "words_dictionary.json"
		with open(word_dict_path, "r") as english_dictionary:
			valid_words = json.load(english_dictionary)
		grams = grams[grams.apply(lambda x: valid_words.get(x['first'], 0) == 1
										and valid_words.get(x['second'], 0) == 1, axis=1)]
		grams = grams.loc[grams['second'] != "n't"]

	grams = grams.reset_index(drop=True)
	grams.to_pickle("./resources/words.pkl")
	return grams


def check_cache(start_word):
	"""
	Analyze the word and the cached tries. Choose the appropriate category for the word
	and create(and store)/load associated trie.
	:param start_word: word to complete
	:return: the loaded trie
	"""
	try:
		pop_trie = open('./resources/popular_trie.pkl', 'rb')
		pop_dict = open('./resources/dict.pkl', 'rb')
		popular_dict = pickle.load(pop_dict)

	except IOError:
		popular_trie()
		pop_trie = open('./resources/popular_trie.pkl', 'rb')
		pop_dict = open('./resources/dict.pkl', 'rb')
		popular_dict = pickle.load(pop_dict)

	if len(start_word) == 1 or start_word in popular_dict:
		triee = pickle.load(pop_trie)
		print(triee)
		return triee, popular_dict

	try:
		long = open('./resources/trie.pkl', 'rb')
	except IOError:
		load_data()
		long = open('./resources/trie.pkl', 'rb')

	return pickle.load(long), popular_dict


def load_data(branch_limit=10000):
	"""
	Load the longest version of the trie, containing most n-grams(limited by the branch_limit)
	:param branch_limit: the limit of children for each node of the trie. Default 10000
	:return: the trie, which also gets stored on the drive
	"""
	try:
		grams = pd.read_pickle('./resources/words.pkl')
	except IOError:
		grams = load_words()

	grams = grams.sort_values(by='freq', ascending=False)

	# Limit the number of children for each node
	grams = grams.groupby("first").head(branch_limit)

	# The transformation from int to a singular tuple is required by the trie API
	grams['freq'] = grams['freq'].apply(lambda x: (x,))

	freqs = grams['freq'].values
	phrases = grams['first'] + " " + grams['second']
	fmt = "@i"
	phrases = list(map(lambda x: np.unicode(x), phrases))
	triee = marisa.RecordTrie(fmt, zip(phrases, freqs))

	# Store the trie
	with open('./resources/trie.pkl', 'wb') as output:
		pickle.dump(triee, output, pickle.HIGHEST_PROTOCOL)
	return triee


def one_letter():
	"""
	Generate a trie that is used for a special case where only one letter is given
	to the autocomplete function. Since it's very expensive to go over all combinations
	each time, this function does it once and stores the result.
	:return: a one-letter trie, which also gets stored on the drive
	"""
	try:
		grams = pd.read_pickle('./resources/words.pkl')
	except IOError:
		grams = load_words()

	short_grams = grams.copy()
	# short_grams['first'] = short_grams[['first']].apply(lambda x: x[0].lower())
	short_grams['indices'] = short_grams.index

	res = short_grams.groupby("first").apply(lambda group: group.nlargest(50, columns='freq'))
	indices = res['indices'].values
	grams = grams.iloc[indices, :]
	grams['freq'] = grams['freq'].apply(lambda x: (x,))

	freqs = grams['freq'].values
	phrases = grams['first'] + " " + grams['second']
	fmt = "@i"
	phrases = list(map(lambda x: np.unicode(x), phrases))
	triee = marisa.RecordTrie(fmt, zip(phrases, freqs))
	with open('./resources/short_trie.pkl', 'wb') as output:
		pickle.dump(triee, output, pickle.HIGHEST_PROTOCOL)
	return triee


def popular_trie():
	"""
	Generate a trie for the most popular words, like "to", "the", etc.
	Popular trie should be used if the branching factor for the long trie is large (>1000)
	:return: a popular trie, which also gets stored on the drive
	"""
	try:
		grams = pd.read_pickle('./resources/words.pkl')
	except IOError:
		grams = load_words()

	big_ones = dict()
	for elem in (grams.groupby(['first']).sum()).iterrows():
		count = elem[1]['freq']
		if count > 7000:
			big_ones[elem[1].name] = count
	grams = grams.loc[grams['first'].isin(big_ones)]
	grams = grams.loc[grams['freq'] > 1000]

	grams['freq'] = grams['freq'].apply(lambda x: (x,))

	freqs = grams['freq'].values
	phrases = grams['first'] + " " + grams['second']
	fmt = "@i"
	phrases = list(map(lambda x: np.unicode(x), phrases))
	triee = marisa.RecordTrie(fmt, zip(phrases, freqs))
	with open('./resources/popular_trie.pkl', 'wb') as output:
		pickle.dump(triee, output, pickle.HIGHEST_PROTOCOL)
	with open('./resources/dict.pkl', 'wb') as output:
		pickle.dump(big_ones, output, pickle.HIGHEST_PROTOCOL)

	return triee


if __name__ == "__main__":
	start = time.time()
	load_words(check_grammar=True)
	load_data()
	popular_trie()


