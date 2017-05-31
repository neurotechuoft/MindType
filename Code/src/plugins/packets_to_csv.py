import csv
import timeit
import datetime

import plugin_interface as plugintypes
from biosignals.BioSignal import BioSignal


class PluginPacketsToCSV(plugintypes.IPluginExtended):
    #
    #
    # # __init__
    # def activate(self):
    # 	self.array = []
    #
    # # Called with each new sample
    # def __call__(self, sample):
    #
    # 	if sample:
    #
    # 		#FORMAT OF INCOMING DATA: ID: %f\n%s\n%s" %(sample.id, str(sample.channel_data)[1:-1], str(sample.aux_data)[1:-1])
    #
    # 		key_values_row = []
    #
    # 		# Create an array of : (sample number, s1, s2 ... s8)
    #
    # 		key_values_row.append(sample.id)
    #
    # 		for i in sample.channel_data:
    # 		    key_values_row.append(i)
    #
    # 		# Append row to self.array
    # 		self.array.append(key_values_row)
    #
    # 		if len(self.array) == 512:
    # 		    print self.array
    # 		    print "Yahhaaayyyyy"
    #
    # 		    self.array = []

    # def __init__(self, file_name="collect.csv", delim = ",", verbose=False):
    # 	now = datetime.datetime.now()
    # 	self.time_stamp = '%d-%d-%d_%d-%d-%d'%(now.year,now.month,now.day,now.hour,now.minute,now.second)
    # 	self.file_name = self.time_stamp
    # 	self.start_time = timeit.default_timer()
    # 	self.delim = delim
    # 	self.verbose = verbose
    #
    #
    # def activate(self):
    #     #self.array_packet = 23
    #
    # 	if len(self.args) > 0:
    # 		if 'no_time' in self.args:
    # 			self.file_name = self.args[0]
    # 		else:
    # 			self.file_name = self.args[0] + '_' + self.file_name;
    # 		if 'verbose' in self.args:
    # 			self.verbose = True
    #
    # 	self.file_name = self.file_name + '.csv'
    # 	print "Will export CSV to:", self.file_name
    # 	#Open in append mode
    # 	with open(self.file_name, 'a') as f:
    # 		f.write('%'+self.time_stamp + '\n')
    #
    # def deactivate(self):
    # 	print "Closing, CSV saved to:", self.file_name
    # 	return
    #
    # def show_help(self):
    # 	print "Optional argument: [filename] (default: collect.csv)"
    #
    # def __call__(self, sample):
    #
    # 	t = timeit.default_timer() - self.start_time
    #
    # 	#print timeSinceStart|Sample Id
    # 	if self.verbose:
    # 		print("CSV: %f | %d" %(t,sample.id))
    #
    # 	row = ''
    # 	row += str(t)
    # 	row += self.delim
    # 	row += str(sample.id)
    # 	row += self.delim
    # 	for i in sample.channel_data:
    # 		row += str(i)
    # 		row += self.delim
    # 	for i in sample.aux_data:
    # 		row += str(i)
    # 		row += self.delim
    # 	#remove last comma
    # 	row += '\n'
    # 	with open(self.file_name, 'a') as f:
    # 		f.write(row)



    # # __init__
    # def activate(self):
    # 	self.array = []
    # 	self.file_name = "packets.csv"
    #
    # 	now = datetime.datetime.now()
    # 	self.time_stamp = '%d-%d-%d_%d-%d-%d'%(now.year,now.month,now.day,now.hour,now.minute,now.second)
    #
    # 	# Wipe file
    # 	with open(self.file_name, 'w') as f:
    # 		f.truncate()
    # 		f.close()
    #
    # 	# Open in append mode
    # 	with open(self.file_name, 'a') as f:
    # 		f.write('%'+self.time_stamp + '\n')
    #
    # # Called with each new sample
    # def __call__(self, sample):
    #
    # 	if sample:
    #
    # 		#FORMAT OF INCOMING DATA: ID: %f\n%s\n%s" %(sample.id, str(sample.channel_data)[1:-1], str(sample.aux_data)[1:-1])
    #
    # 		key_values_row = []
    #
    # 		# Create an array of : (sample number, s1, s2 ... s8)
    # 		key_values_row.append(sample.id)
    #
    # 		for i in sample.channel_data:
    # 		    key_values_row.append(i)
    #
    # 		# Append row to self.array
    # 		self.array.append(key_values_row)
    #
    # 		# Once 2 secs of data collected, wipe old CSV and write in new data
    # 		if len(self.array) == 512:
    #
    # 			# # Wipe file
    # 			# with open(self.file_name, 'w') as f:
    # 			# 	f.truncate()
    # 			# 	f.close()
    # 			#
    # 			# Write in new data
    # 			# with open(self.file_name, 'a') as f:
    # 			#
    # 			# 	for row in self.array:
    # 			# 		f.write(row)
    #
    # 		    print self.array
    # 		    print "Yahhaaayyyyy\n\n\n"
    #
    # 		    self.array = []

    def __init__(self, file_name="packets.csv", delim=",", verbose=False):
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
                self.file_name = self.args[0] + '_' + self.file_name
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

    def __call__(self, sample, objects_to_update=None):
        self.num_of_samples += 1
        t = timeit.default_timer() - self.start_time

        # print timeSinceStart|Sample Id
        if self.verbose:
            print("CSV: %f | %d" % (t, sample.id))
        data = []
        row = ''
        row += str(t)
        row += self.delim

        row += str(sample.id)
        row += self.delim

        for i in sample.channel_data:
            row += str(i)
            row += self.delim

        data = row.split(",")

        # print(data)

        # UPDATE OBJECTS
        for obj in objects_to_update:
            if isinstance(obj, BioSignal):
                obj.update(data)

        # WRITE TO CSV
        # Save 10 seconds of data
        if self.num_of_samples <= 512:
            # row = ''
            # row += str(t)
            # row += self.delim
            #
            # row += str(sample.id)
            # row += self.delim
            #
            # for i in sample.channel_data:
            #     row += str(i)
            #     row += self.delim

            row += '\n'

            # open, write, and close
            with open(self.file_name, 'a') as f:
                f.write(row)

        else:
            print "Time to wipe :D\n\n\n"

            # Wipe file
            with open(self.file_name, 'w') as f:
                f.truncate()

            self.num_of_samples = 0
