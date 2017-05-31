import plugin_interface as plugintypes
import numpy
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time


class PluginPrint(plugintypes.IPluginExtended):
    def __init__(self, file_name="collect.csv", delim=",", verbose=False):
        now = datetime.datetime.now()
        self.time_stamp = '%d-%d-%d_%d:%d:%d' % (
            now.year, now.month, now.day, now.hour, now.minute, now.second)
        self.file_name = 'collect-' + self.time_stamp
        self.start_time = timeit.default_timer()
        self.delim = delim
        self.verbose = verbose
        self.fig = plt.figure()

    def activate(self):
        if len(self.args) > 0:
            if 'no_time' in self.args:
                self.file_name = self.args[0]
            else:
                self.file_name = self.args[0] + '_' + self.file_name;
            if 'verbose' in self.args:
                self.verbose = True

        self.file_name = self.file_name + '.csv'
        print "Will export CSV to:", self.file_name

        # Preparing graph
        ax1 = self.fig.add_subplot(1, 1, 1)

        # Open in append mode
        with open(self.file_name, 'a') as f:
            f.write('%' + self.time_stamp + '\n')

    def deactivate(self):
        print "Closing, CSV saved to:", self.file_name
        return

    def show_help(self):
        print "Optional argument: [filename] (default: collect.csv)"

    def __call__(self, sample):
        '''
        For given instance, obtain data from OpenBCI and a) save to .CSV, and 
        b) update the graph.
        '''
        t = timeit.default_timer() - self.start_time

        # print timeSinceStart|Sample Id
        if self.verbose:
            print("CSV: %f | %d" % (t, sample.id))

        row = ''
        row += str(t)
        row += self.delim
        row += str(sample.id)
        row += self.delim
        for i in sample.channel_data:
            row += str(i)
            row += self.delim
        for i in sample.aux_data:
            row += str(i)
            row += self.delim
        # remove last comma
        row += '\n'
        with open(self.file_name, 'a') as f:
            f.write(row)

        ani = animation.FuncAnimation(self.fig, animate, interval=1000)
        plt.show()

    def animate(i):
        '''
        Live graph using matplotlib, pulling from csv file.
        '''
        pullData = open(self.file_name, "r").read()
        dataArray = pullData.split('\n')
        xar = []
        yar = []
        for eachLine in dataArray:
            if len(eachLine) > 1:
                x, y = eachLine.split(',')
                xar.append(int(x))
                yar.append(int(y))
        ax1.clear()
        ax1.plot(xar, yar)
