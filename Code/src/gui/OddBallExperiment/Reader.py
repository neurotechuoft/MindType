"""
csv file reader
"""
import csv
import matplotlib.pyplot as plt

"""
Each second, we get 220 samples, with each sample having 4 voltages
for 26.9 seconds we have 5934 samples, (1/10 second extra)
"""
def csv_reader(file_obj):
    array = []
    reader = csv.reader(file_obj)
    for row in reader:
        thing = row[1:]
        if " /muse/eeg" in thing:

            array.append(thing)
    return array

with open('test_record_1.csv') as f:

    eeg_data = csv_reader(f)

print(len(eeg_data))

electrode1 = []
electrode2 = []
electrode3 = []
electrode4 = []

for sample in eeg_data:

    electrode1.append(float(sample[1]))
    electrode2.append(float(sample[2]))
    electrode3.append(float(sample[3]))
    electrode4.append(float(sample[4]))

fig = plt.figure()

ax1 = fig.add_subplot(221)
ax1.plot(electrode1, 'r-')

ax2 = fig.add_subplot(222)
ax2.plot(electrode2, 'k-')

ax3 = fig.add_subplot(223)
ax3.plot(electrode3, 'b-')

ax4 = fig.add_subplot(224)
ax4.plot(electrode4, 'g-')
plt.show()
