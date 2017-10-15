# MindType
EEG Speller

## Setup
1. Install Miniconda
2. Create a Conda environment
3. Install scipy, numpy using conda Install
4. Install everything else using pip

## Usage:
To use multithreaded framework:
'''
    sudo python main.py -p /dev/ttyUSB0 --add pub_sub
'''

To use multithreaded framework and save to CSV (temporary solution):
'''
    sudo python main.py -p /dev/ttyUSB0 --add pub_sub csv_collect
'''

## Plan
![Plan](Meetings/resources/2017-07-17.png?raw=true "Plan")

## Research Papers
### Phase 1 (P300)
- https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3175727/
    - "Comparison of Classification Methods for P300 Brain-Computer Interface on Disabled Subjects"
### Phase 2 (Binary motor classification)
- http://iopscience.iop.org/article/10.1088/1741-2560/10/4/046003/pdf
    - "Quadcopter control in three-dimensional space using a noninvasive motor imagery-based brain–computer interface"
### Phase 3 (Multiclass motor classification)
- http://ieeexplore.ieee.org/document/6943840/?reload=true
    - **"Discriminating hand gesture motor imagery tasks using cortical current density estimation"**
- http://www.sciencedirect.com/science/article/pii/S0167876015001749#fn0010
    - Explanation of surface laplacian and applications to EEG
