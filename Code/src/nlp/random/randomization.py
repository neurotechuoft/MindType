import codecs
import random

#with codecs.open('./w2_.txt', "r", encoding='utf-8', errors='ignore')  as source:
#    data = [ (random.random(), line) for line in source ]

#with open('randomized_result','w') as target:
#    for _, line in data:
#        target.write( line )
#random.shuffle(data)
#train_data = data[:int((len(data) + 1) * .999)]  # Remaining 80% to training set
#test_data = data[int(len(data) * .999 + 1):]  # Splits 20% data to test set


for i in range(2,6):
    test_path = './w'+str(i)+'_.txt'
    with codecs.open(test_path, "r", encoding='utf-8',
                     errors='ignore')  as source:
        data = [(random.random(), line) for line in source]

    random.shuffle(data)
    train_data = data[:int((len(data) + 1) * .999)]  # Remaining 80% to training set
    test_data = data[int(len(data) * .999 + 1):]  # Splits 20% data to test set
    #Save data to desire file
    train_store = 'train_data_w'+str(i)
    with open(train_store, 'w') as target:
        for (_, line) in train_data:
            target.write(line)
    test_store = 'test_data_w' + str(i)
    with open(test_store, 'w') as target:
        for (_, line) in test_data:
            target.write(line)


'''
import random
with codecs.open('./w3_.txt', "r", encoding='utf-8', errors='ignore')  as source:
    data = [ (random.random(), line) for line in source ]
#data.sort()
with open('another_file','w') as target:
    for _, line in data:
        target.write( line )


file = open("datafile.txt", "r")
data = list()
for line in file:
    data.append(line.split(  # your preferred delimiter))
        file.close()
    random.shuffle(data)
    train_data = data[:int((len(data) + 1) * .80)]  # Remaining 80% to training set
    test_data = data[int(len(data) * .80 + 1):]  # Splits 20% data to test set

'''

'''
from nltk import ngrams

sentence = 'this is a foo bar sentences, and i want to ongranize it. I\'ve eaten too much'
n = 2
bigrams = ngrams(sentence.split(), n)
for grams in bigrams:
    print(grams)
'''

'''
with codecs.open('./w3_.txt', "r", encoding='utf-8', errors='ignore') as fdata:
    grams = pd.read_table(fdata, names=["freq", "first", "second"])

grams = grams.sort_values(by='freq', ascending=False)
random.sample(population, k)
'''

