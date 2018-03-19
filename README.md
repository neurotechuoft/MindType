# MindType
A mind-controlled keyboard using imagined sign language.

Communication, especially via keyboard, is very difficult, if not impossible, for people with various neuromuscular degenerative diseases and muscular dystrophy. Because of this, EEG spellers based on the [P300](https://en.wikipedia.org/wiki/P300_(neuroscience)) [oddball paradigm](https://en.wikipedia.org/wiki/Oddball_paradigm) have been made and researched upon for many years. Current EEG spellers are quite slow (~50 bits/min, or 6 letters/min with NLP optimizations) [1] [2]. It becomes impossible for a person with such conditions to enjoy a conversation with their loved ones due to the low bit rate.

MindType seeks to improve the bit rate of mind-controlled keyboards. It also uses a grid system, like [traditional P300 spellers](http://iopscience.iop.org/1741-2552/13/6/066018/downloadHRFigure/figure/jneaa47eff2). However, each row and column will have a numerical id (1-6), which is mapped to a hand gesture. A letter is selected by imagining the appropriate gesture for each hand (left controls rows, right controls columns). This ensures that it takes 1 operation to choose each letter (current systems take at least 3 operations per gesture from our initial research). Additionally, the use of NLP algorithms would boost the bit rate by attempting to predict the word the user wants to enter. This allows for many cases where the user wouldn't have to type the full word.

[1] https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3679217/

[2] https://www.ncbi.nlm.nih.gov/pubmed/12853169


## Hardware necessary:
OpenBCI Cyton. (The board works with Muse as well, but you would need to use P300 instead of motor imagery)


## Setup
1. Clone the project
2. Go into './Code/src'
3. Run setup.sh


## Usage:
To use MindType:
```
    ./MindType.sh
```

To toggle different features, you can change the feature flags in "./Code/src/feature_flags.py"


## Citations
(See Plan section below for more details)
### Phase 1: P300 keyboard
- https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3175727/
    - "Comparison of Classification Methods for P300 Brain-Computer Interface on Disabled Subjects"
- http://alexandre.barachant.org/blog/2017/02/05/P300-with-muse.html
    - Thanks to Alexandre Barachant for his P300 script on Muse! Unfortunately it was on Muse 2016, so we made a Muse 2014 version of it
### Phase 2: Binary motor classification
- http://iopscience.iop.org/article/10.1088/1741-2560/10/4/046003/pdf
    - "Quadcopter control in three-dimensional space using a noninvasive motor imagery-based brain–computer interface"
### Phase 3: Multiclass motor classification
- http://ieeexplore.ieee.org/document/6943840/?reload=true
    - **"Discriminating hand gesture motor imagery tasks using cortical current density estimation"**
        - http://www.sciencedirect.com/science/article/pii/S0167876015001749#fn0010
            - Explanation of surface laplacian and applications to EEG
- http://www.tandfonline.com/doi/abs/10.1080/10790268.2017.1369215
    - **"Prediction of specific hand movements using EEG signals"**
- 
        
## Multithreaded architecture (MTA)
The whole program has two basic functions: collect data from the board, and process it somehow. If this were to be done in a single-threaded application, if one iteration of processing were to take too long, it would block the program from receiving data from the board. Due to this, the program uses a multithreaded architecture, with one thread responsible for collecting data and one thread responsible for processing it.

The MTA uses a variant of the publish-subscribe design pattern. A messaging queue is implemented in the Controller class. Controllable classes **can be controlled** by receiving messages in their Controller, and handing the message however appropriate. A master Controller is responsible for receiving instructions from the user and passing them along to each Controllable.

A BioSignal is a Controllable that can also **update** itself with the latest data sample from the board, and **process** data somehow. During each update cycle, it also calls its **control()** method. The updating and processing will occur on separate threads instantiated in the **main()** function. (Look at the Tagger class for an example of a BioSignal).

**main.py** initates the program, which is controlled from the GUI. It first sets up the OpenBCI board, makes the GUI, and then sets up a thread for processing. The GUI then handles playing / pausing the board by instantiating a thread to run **stream()** from openbci_v3. This function streams biosignals from the OpenBCI board, and calls each BioSignals's **update()** function). Processing of BioSignals is handled in **process_thread** (which runs **run_processor()**) by asynchronously calling each BioSignal's process function.

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


## Plan
![Plan](Meetings/resources/2017-07-17.png?raw=true "Plan")
