import timeit

import plugin_interface as plugintypes
from biosignals.biosignal import BioSignal


class PluginPrint(plugintypes.IPluginExtended):
    def __init__(self):
        self.start_time = timeit.default_timer()
        self.delim = ','

    def activate(self):
        print("Print activated")

    # called with each new sample
    def __call__(self, sample, objects_to_update=None):
        t = timeit.default_timer() - self.start_time

        # print timeSinceStart|Sample Id
        # if self.verbose:
        # 	print("CSV: %f | %d" % (t, sample.id))
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
        print("Received data")

        # UPDATE OBJECTS
        if objects_to_update is not None:
            for obj in objects_to_update:
                if isinstance(obj, BioSignal):
                    obj.update(data)
