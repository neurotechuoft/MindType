# third-party library
import torch
import torch.nn as nn
import torch.optim as optim
from torch.autograd import Variable
import csv
import numpy as np
import random
import os


class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()

        # Define height = time; width = # of channels
        self.spectral_conv = nn.Sequential(
            # TIME CONVOLUTION
            nn.Conv2d(
                in_channels=1,
                out_channels=25,  # 25 Linear Units
                kernel_size=(10, 1),  # Convolve 10 samples from 1 channel
                stride=1
            ),
            # SPATIAL FILTER
            nn.Conv2d(
                in_channels=25,
                out_channels=25,  # 25 Exponential Linear Units
                kernel_size=(1, 8),  # Convolve 1 sample from 8 channels
                stride=1
            ),
            nn.ELU(),

            # MAX-POOL
            nn.MaxPool2d(
                kernel_size=(3, 1)  # ??? need to try
            )
        )

        self.regular_conv_1 = nn.Sequential(
            nn.Conv2d(
                in_channels=25,
                out_channels=50,  # (as per paper)
                kernel_size=(10, 1),
                stride=1,
            ),
            nn.ELU(),
            nn.MaxPool2d(
                kernel_size=(3, 1)
            )
        )

        self.regular_conv_2 = nn.Sequential(
            nn.Conv2d(
                in_channels=50,
                out_channels=100,  # (as per paper)
                kernel_size=(10, 1),
                stride=1,
            ),
            nn.ELU(),
            nn.MaxPool2d(
                kernel_size=(3, 1)
            )
        )

        self.regular_conv_3 = nn.Sequential(
            nn.Conv2d(
                in_channels=100,
                out_channels=200,  # (as per paper)
                kernel_size=(10, 1),
                stride=1,
            ),
            nn.ELU(),
            nn.MaxPool2d(
                kernel_size=(3, 1)
            )
        )

        self.out = nn.Sequential(
            nn.Linear(200 * 8, 10),  # 10 gestures to classify
            nn.Softmax()
        )

    def forward(self, x):
        x = self.spectral_conv(x)
        x = self.regular_conv_1(x)
        x = self.regular_conv_2(x)
        x = self.regular_conv_3(x)
        x = x.view(x.size(0), -1)  # flatten before passing to Softmax layer
        output = self.out(x)

        return output


# For each 512-step sample, use 20 crops: 10 backwards and 10 forwards
#   - Assume that frequencys of beta are most important -> ~20Hz
#   - Then need to have 1/20 * 256Hz -> 12.5 ~ 10 samples
def load_data(filepath):
    samples = np.empty((0, 10), np.dtype('d'))
    with open(filepath, "r") as data_file:
        data_reader = csv.reader(data_file, delimiter=",", quotechar="|")
        i = 0
        for row in data_reader:
            # 0.17300988500028325,0,-161615.9870166763,-162619.44623225287,-159844.94654476005,-161439.18471803484,-162225.787308906,-162100.12580157828,-160387.64690013492,-162823.80823180775,,0
            samples = np.append(samples, [
                [i, float(row[2]), float(row[3]), float(row[4]), float(row[5]),
                 float(row[6]), float(row[7]), float(row[8]), float(row[9]),
                 int(row[11])]], axis=0)
            i += 1
    return samples


def extract_packets(samples, sample_rate, num_channels):
    ret_packets = np.empty((0, int(4 * sample_rate), num_channels),
                           dtype=np.dtype('d'))
    ret_labels = np.empty((0, 10))

    curr_packet = np.empty((0, num_channels))

    next_packet = np.empty((0, num_channels))
    filling_next_packet = False
    gesture_full = False

    curr_gesture = samples[0, -1]
    gesture = curr_gesture

    for i in range(0, samples.shape[0]):

        if samples[i, -1] != curr_gesture and curr_gesture == 0:
            gesture_full = True
            gesture = samples[i, -1]

        # If packet full, save packet
        if curr_packet.shape[0] == int(4 * sample_rate):
            ret_packets = np.append(ret_packets, [curr_packet], axis=0)
            label = np.zeros(10)
            label[int(gesture)] = 1
            ret_labels = np.append(ret_labels, [label], axis=0)

            # Multiple crops: add to beginning
            new_crop = np.copy(curr_packet)
            for crop in range(1, 21):
                new_crop = np.delete(new_crop, -1, axis=0)
                new_crop = np.insert(
                    new_crop, 0, [ret_packets[-1, -1 * crop,]], axis=0
                )
                ret_packets = np.append(ret_packets, [new_crop], axis=0)
                ret_labels = np.append(ret_labels, [label], axis=0)

            # Multiple crops: add to end
            new_crop = np.copy(curr_packet)
            for crop in range(20):
                new_crop = np.delete(new_crop, 0, axis=0)
                new_crop = np.insert(
                    new_crop, -1, [samples[i + crop]], axis=0
                )
                ret_packets = np.append(ret_packets, [new_crop], axis=0)
                ret_labels = np.append(ret_labels, [label], axis=0)

            gesture_full = False
            # If was filling two packets, discard current packet and continue
            #  filling next packet
            if filling_next_packet:
                curr_packet = np.copy(next_packet)
                next_packet = np.empty((0, num_channels))
            else:
                curr_packet = np.empty((0, num_channels))
        # If we added all the gesture samples, but packet isn't full, borrow
        # samples from next packet
        elif gesture_full:
            next_packet = np.append(next_packet, [samples[i]], axis=0)
            filling_next_packet = True

        # Load samples into packet
        curr_packet = np.append(curr_packet, [samples[i]], axis=0)

    return ret_packets, ret_labels


def split_data_into_training_test(loaded_packets, labels, batch_size,
                                  sample_rate, num_channels):
    training_data = {}
    training_packets = np.empty((0, batch_size, 1, int(4 * sample_rate),
                                 num_channels),
                                dtype=np.dtype('d'))
    training_labels = np.empty((0, batch_size, 10))
    curr_training_packet_batch = np.empty((0, 1, int(4 * sample_rate),
                                           num_channels),
                                          dtype=np.dtype('d'))
    curr_training_label_batch = np.empty((0, 10))

    test_data = {}
    test_packets = np.empty((0, batch_size, 1, int(4 * sample_rate),
                             num_channels),
                            dtype=np.dtype('d'))
    test_labels = np.empty((0, batch_size, 10))
    curr_test_packet_batch = np.empty((0, 1, int(4 * sample_rate),
                                       num_channels),
                                      dtype=np.dtype('d'))
    curr_test_label_batch = np.empty((0, 10))

    for i in range(loaded_packets.shape[0]):
        input_np = np.copy(loaded_packets[i])
        input_np = np.delete(input_np, 0, axis=1)
        input_np = np.delete(input_np, -1, axis=1)
        input_np = np.expand_dims(input_np, axis=0)
        # input_np = np.expand_dims(input_np, axis=0)

        put_in_training_set = random.randint(1, 10) <= 7

        if put_in_training_set:

            if curr_training_packet_batch.shape[0] == 40:
                training_packets = np.append(training_packets,
                                             [curr_training_packet_batch],
                                             axis=0)
                training_labels = np.append(training_labels,
                                            [curr_training_label_batch],
                                            axis=0)

                curr_training_packet_batch = np.empty(
                    (0, 1, int(4 * sample_rate),
                     num_channels),
                    dtype=np.dtype('d'))
                curr_training_label_batch = np.empty((0, 10))

            curr_training_packet_batch = np.append(curr_training_packet_batch,
                                                   [input_np],
                                                   axis=0)
            curr_training_label_batch = np.append(curr_training_label_batch,
                                                  [labels[i]],
                                                  axis=0)
        else:
            if curr_test_packet_batch.shape[0] == 40:
                test_packets = np.append(test_packets,
                                         [curr_test_packet_batch],
                                         axis=0)
                test_labels = np.append(test_labels,
                                        [curr_test_label_batch],
                                        axis=0)

                curr_test_packet_batch = np.empty((0, 1, int(4 * sample_rate),
                                                   num_channels),
                                                  dtype=np.dtype('d'))
                curr_test_label_batch = np.empty((0, 10))

            curr_test_packet_batch = np.append(curr_test_packet_batch,
                                               [input_np],
                                               axis=0)
            curr_test_label_batch = np.append(curr_test_label_batch,
                                              [labels[i]],
                                              axis=0)

    training_data["packets"] = training_packets
    training_data["labels"] = training_labels

    test_data["packets"] = test_packets
    test_data["labels"] = test_labels

    return training_data, test_data


def train(cnn, training_data):
    # criterion = nn.CrossEntropyLoss()
    criterion = nn.L1Loss()
    optimizer = optim.SGD(cnn.parameters(), lr=0.001, momentum=0.9)

    running_loss = 0.0
    for epoch in range(2):
        for batch_id in range(training_data["packets"].shape[0]):
            batch_packet_tensor = Variable(torch.from_numpy(
                training_data["packets"][batch_id])
            ).float()

            batch_target_label_tensor = Variable(torch.from_numpy(
                training_data["labels"][batch_id])
            ).float()

            optimizer.zero_grad()

            # Forward + backward + optimize
            batch_output = cnn(batch_packet_tensor)
            # loss = criterion((batch_output.max(0)[1]).float(),
            #                  (batch_target_label_tensor.max(0)[1]).long())
            loss = criterion(batch_output.float(),
                             batch_target_label_tensor.float())
            loss.backward()
            optimizer.step()

            # print statistics
            running_loss += loss.data[0]
            # if batch_id % 100 == 99:  # print every 2000 mini-batches
            print('[%d, %5d] loss: %.3f' %
                  (epoch + 1, batch_id + 1, running_loss / (batch_id + 1)))


def main():
    # time = np.array([])
    # index = np.array([])
    # c4 = np.array([])
    # c3 = np.array([])
    # gesture = np.array([])

    training_samples_dir = "../../Data-Repository/eeg/motor-imagery/" \
                           "preprocessed/2018-03-17/"

    num_channels = 8
    sample_rate = 256.0
    batch_size = 40
    cnn = CNN()
    training_data = {}
    test_data = {}

    training_data["packets"] = np.empty((0, batch_size, 1, int(4 * sample_rate),
                                         num_channels),
                                        dtype=np.dtype('d'))
    training_data["labels"] = np.empty((0, batch_size, 10))

    test_data["packets"] = np.empty((0, batch_size, 1, int(4 * sample_rate),
                                     num_channels),
                                    dtype=np.dtype('d'))
    test_data["labels"] = np.empty((0, batch_size, 10))

    filecount = 0
    for filename in os.listdir(training_samples_dir):
        if filecount < 1 and filename.endswith(".csv"):
            file = os.path.join(training_samples_dir, filename)

            samples = load_data(file)
            print("Loaded data...")
            loaded_packets, labels = extract_packets(samples, sample_rate, 10)

            print("Extracted packets...")
            curr_training_data, curr_test_data = \
                split_data_into_training_test(loaded_packets,
                                              labels,
                                              batch_size,
                                              sample_rate,
                                              num_channels)
            training_data["packets"] = np.append(training_data["packets"],
                                                 curr_training_data["packets"],
                                                 axis=0)
            training_data["labels"] = np.append(training_data["labels"],
                                                curr_training_data["labels"],
                                                axis=0)

            test_data["packets"] = np.append(test_data["packets"],
                                             curr_test_data["packets"],
                                             axis=0)
            test_data["labels"] = np.append(test_data["labels"],
                                            curr_test_data["labels"],
                                            axis=0)
            print("DONE: extracting packets")
        filecount += 1

    print("Training data packets: " + str(training_data["packets"].shape))
    print("Training data labels: " + str(training_data["labels"].shape))

    print("Test data packets: " + str(test_data["packets"].shape))
    print("Test data labels: " + str(test_data["labels"].shape))


    print("Starting training...")
    train(cnn, training_data)
    print("Finished training :D")

    # Expected shape of tensor: (batch, channels, height, width)
    # input_np = loaded_packets[0]
    # input_np = np.delete(input_np, 0, axis=1)
    # input_np = np.delete(input_np, -1, axis=1)
    # input_np = np.expand_dims(input_np, axis=0)
    # input_np = np.expand_dims(input_np, axis=0)
    input_tensor = Variable(torch.from_numpy(
        test_data["packets"][0])).float()
    print(input_tensor.size())

    print("Running CNN...")
    out = cnn(input_tensor)
    print("DONE: running sample through CNN")
    print("Predicted: " + str(out))
    print("Actual: " + str(test_data["labels"][0]))


if __name__ == '__main__':
    main()
