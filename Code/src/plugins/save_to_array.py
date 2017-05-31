import plugin_interface as plugintypes

class PluginSaveToArray(plugintypes.IPluginExtended):
    
    # __init__
	def activate(self):
		print "Print activated"
		self.array = []
	
	# Called with each new sample
	def __call__(self, sample):
	    
		if sample:
		    
			#FORMAT OF INCOMING DATA: ID: %f\n%s\n%s" %(sample.id, str(sample.channel_data)[1:-1], str(sample.aux_data)[1:-1])
			
			key_values_row = []
			
			# Create an array of : (sample number, s1, s2 ... s8)
			
			key_values_row.append(sample.id)
			
			for i in sample.channel_data:
			    key_values_row.append(i)
			
			# Append row to self.array
			self.array.append(key_values_row)
			
			if len(self.array) == 512:
			    print self.array
			    print "Yahhaaayyyyy"
			    
			    self.array = []
			    
			

