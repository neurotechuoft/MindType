import csv
import timeit
import datetime

import plugin_interface as plugintypes


class PluginInitNonfocused(plugintypes.IPluginExtended):
    def __init__(self, file_name="init_nonfocused.csv", delim=",",
                 verbose=False):
        init_time = datetime.datetime.now()
        now_time = datetime.datetime.now()
        self.file_name = file_name
        self.start_time = timeit.default_timer()
        self.delim = delim
        self.verbose = verbose

    def activate(self):
        self.num_of_samples = 0

        # Wipe file
        with open(self.file_name, 'w') as f:
            f.truncate()
            f.close()

        if len(self.args) > 0:
            if 'no_time' in self.args:
                self.file_name = self.args[0]
            else:
                self.file_name = self.args[0] + '_' + self.file_name;
            if 'verbose' in self.args:
                self.verbose = True

        print "Will export CSV to:", self.file_name

    # Open in append mode
    # with open(self.file_name, 'a') as f:
    # 	f.write('%'+self.time_stamp + '\n')

    def deactivate(self):
        print "Closing, CSV saved to:", self.file_name
        return

    def show_help(self):
        print "Optional argument: [filename] (default: collect.csv)"

    def __call__(self, sample):
        self.num_of_samples += 1

        t = timeit.default_timer() - self.start_time

        # print timeSinceStart|Sample Id
        if self.verbose:
            print("CSV: %f | %d" % (t, sample.id))

        # Save 10 seconds of data
        if self.num_of_samples < 2560:
            row = ''
            row += str(t)
            row += self.delim

            row += str(sample.id)
            row += self.delim

            for i in sample.channel_data:
                row += str(i)
                row += self.delim

            # remove last comma
            row += '\n'
            with open(self.file_name, 'a') as f:
                f.write(row)
