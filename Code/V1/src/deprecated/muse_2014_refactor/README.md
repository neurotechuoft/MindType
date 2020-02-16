# Muse 2014 Refactor
The first required thing is to install and use the muse-io library to successfully connect to the Muse headband.
You will then need the following Python libraries:
- liblo
- pylsl
- mne
- Queue
- (sklearn)

Connect to the muse (ensure the default port is 1234) and run the muse_connect_test.py script in the test-demonstrations 
directory. This is a simple test-script for streaming data from the muse to an lsl outlet. 