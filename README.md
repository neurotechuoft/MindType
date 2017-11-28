# MindType
A mind-controlled keyboard using imagined sign language.

Communication, especially via keyboard, is very difficult if not impossible for people with various neuromuscular degenerative diseases and muscular dystrophy. Because of this, EEG spellers based on the [P300](https://en.wikipedia.org/wiki/P300_(neuroscience)) [oddball paradigm](https://en.wikipedia.org/wiki/Oddball_paradigm) have been made and researched upon for many years. Current EEG spellers are quite slow (~50 bits/min, or 6 letters/min with NLP optimizations) [1] [2]. It becomes impossible for a person with such conditions to enjoy a conversation with their loved ones due to the low bit rate.

MindType seeks to improve the bit rate of mind-controlled keyboards. It also uses a grid system, like [traditional P300 spellers](http://iopscience.iop.org/1741-2552/13/6/066018/downloadHRFigure/figure/jneaa47eff2). However, each row and column would have a numerical id (1-6), which is mapped to a hand gesture. A letter is selected by imagining the appropriate gesture for each hand (left controls rows, right controls columns). This ensures that it takes 1 operation to choose each letter (current systems take at least 3 operations per gesture from our initial research). Additionally, the use of NLP algorithms would boost the bit rate by attempting to predict the word the user wants to enter. This allows for many cases where the user wouldn't have to type the full word.

[1] https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3679217/

[2] https://www.ncbi.nlm.nih.gov/pubmed/12853169


## Setup
**deprecated :'(**
1. Install Miniconda
2. Create a Conda environment
3. Install scipy, numpy using conda Install
4. Install everything else using pip

## Usage:
To use multithreaded framework:
```
    sudo python main.py -p /dev/ttyUSB0 --add pub_sub
```

To use multithreaded framework, tag data, and save to CSV (temporary solution):
```
    sudo python main.py -p /dev/ttyUSB0 --add pub_sub csv_collect
```

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
        - Method 1 of doing MMC
        - http://www.sciencedirect.com/science/article/pii/S0167876015001749#fn0010
            - Explanation of surface laplacian and applications to EEG
- http://www.tandfonline.com/doi/abs/10.1080/10790268.2017.1369215
    - **"Prediction of specific hand movements using EEG signals"**
        - Method 2 of doing MMC
        
## Multithreaded architecture (MTA)
The whole program has two basic functions: collect data from the board, and process it somehow. If this were to be done in a single-threaded application, if one iteration of processing were to take too long, it would block the program from receiving data from the board. Due to this, the program uses a multithreaded architecture, with one thread responsible for collecting data and one thread responsible for processing it.

The MTA uses a variant of the publish-subscribe design pattern. A messaging queue is implemented in the Controller class. Controllable classes **can be controlled** by receiving messages in their Controller, and handing the message however appropriate. A master Controller is responsible for receiving instructions from the user and passing them along to each Controllable.

A BioSignal is a Controllable that can also **update** itself with the latest data sample from the board, and **process** data somehow. During each update cycle, it also calls its **control()** method. The updating and processing will occur on separate threads instantiated in the **main()** function. (Look at the Tagger class for an example of a BioSignal).

**main.py** executes the entire program. It first sets up the OpenBCI board, and then sets up a thread for processing. The main function then handles parsing commands from the user in the **execute_board()** function (which instantiates a thread for calling each BioSignals's **update()** function), and handles processing of the BioSignals in **process_thread** which runs **run_processor()**. The **execute_board()** function calls **start_streaming()** from openbci_v3, which obtains a sample and calls whatever callback function provided when instantiating the program from command line (in this case, *pub_sub.py*). *pub_sub.py* is responsible for providing all the BioSignals with samples that are coming in.

## Contributing
We follow trunk-based development to avoid merge conflicts as much as
possible, and to ensure that code in our master branch is always works.

1. Make a new branch for your **small** feature.
2. Code :D
3. Once your **small** feature is done, make a pull request. If your feature
isn't fully ready, use feature toggling to turn it off
(*feature_flags/feature_flags.py*)
4. Your code will go through a review. Once it passes, merge the pull reqest!
5. Repeat :D