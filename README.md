# MindType
A mind-controlled keyboard using imagined sign language.

Communication, especially via keyboard, is very difficult, if not impossible, for people with various neuromuscular degenerative diseases and muscular dystrophy. Because of this, EEG spellers based on the [P300](https://en.wikipedia.org/wiki/P300_(neuroscience)) [oddball paradigm](https://en.wikipedia.org/wiki/Oddball_paradigm) have been made and researched upon for many years. Current EEG spellers are quite slow (~50 bits/min, or 6 letters/min with NLP optimizations) [1] [2]. It becomes impossible for a person with such conditions to enjoy a conversation with their loved ones due to the low bit rate.

MindType seeks to improve the bit rate of mind-controlled keyboards. It also uses a grid system, like [traditional P300 spellers](http://iopscience.iop.org/1741-2552/13/6/066018/downloadHRFigure/figure/jneaa47eff2). However, each row and column will have a numerical id (1-6), which is mapped to a hand gesture. A letter is selected by imagining the appropriate gesture for each hand (left controls rows, right controls columns). This ensures that it takes 1 operation to choose each letter (current systems take at least 3 operations per gesture from our initial research). Additionally, the use of NLP algorithms would boost the bit rate by attempting to predict the word the user wants to enter. This allows for many cases where the user wouldn't have to type the full word.

[1] https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3679217/

[2] https://www.ncbi.nlm.nih.gov/pubmed/12853169


#### Development status: Work In Progress


## Hardware necessary:
OpenBCI Cyton. (The keyboard works with Muse as well, but you would need to use P300 instead of motor imagery)


## Setup
1. Clone the project
2. Go into './Code/src'
3. Run setup.sh

## Dev Setup
### Front End:
Setup:
1. `npm install`
2. `npm install -g concurrently`
3. `npm install -g wait-on`

To run dev Electron build: 

`npm run electron-dev`


## Usage:
To use MindType:
```
    ./MindType.sh
```

To toggle different features, you can change the feature flags in "./Code/src/feature_flags.py"



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



## Algorithm approaches
(See Plan section below for more details)
### Phase 1: P300 keyboard
We tried to use linear discriminant analysis (LDA) and quadratic discriminant analysis (QDA) to classify P300 from the Muse. We obtained samples between 0.1--0.75s after the stimulus, and passed it to the classifier as a single vector. Unfortunately, we obtained poor results. Upon further investigation, we noticed that time synchronization issues may have decreased the ability of the classifiers to operate properly. To combat this, we plan to use a shallow covolutional neural network to allow for signals to shift in time without affecting classification accuracy.

- https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3175727/
    - "Comparison of Classification Methods for P300 Brain-Computer Interface on Disabled Subjects"
- http://alexandre.barachant.org/blog/2017/02/05/P300-with-muse.html
    - Thanks to Alexandre Barachant for his P300 script on Muse! Unfortunately it was on Muse 2016, so we made a Muse 2014 version of it
### Phase 2: Binary motor classification
- http://iopscience.iop.org/article/10.1088/1741-2560/10/4/046003/pdf
    - "Quadcopter control in three-dimensional space using a noninvasive motor imagery-based brain–computer interface"
### Phase 3: Multiclass motor classification
We used a deep convolutional neural network to classify 9 different hand movements (extension, flexion, suprination, pronation, V sign, Y sign with pinkie and thumb, fist-close, fist-open, and pinch). EEG data was collected using an in-house headset from 8 channels (F3, Fz, F4, C3, C1, Cz, C2, C4) at a sampling frequency of 256Hz using the OpenBCI without electrode amplifiers. [3] showed the first four movements being distinguished through EEG, and [4] showed the last 5 movements being distinguished through EEG. Our neural network architecture was inspired by the deep CNN shown in [5]. We collected 60 4-second samples of data for each gesture (see [6] for more details).

In the future, we plan to obtain data using the OpenBCI WiFi Shield to increase our temporal resolution to 1000Hz. In addition, we plan on using 3D convolutions (time, spatial-x, spatial-y). This will allow convolutions to be done over spatial-x and spatial-y, which may allow the CNN to understand the propogation of electric field through space for better source localization.

- http://ieeexplore.ieee.org/document/6943840/?reload=true
    - [3]: **"Discriminating hand gesture motor imagery tasks using cortical current density estimation"**
        - Aproach 1 for Phase 3
        - http://www.sciencedirect.com/science/article/pii/S0167876015001749#fn0010
            - Explanation of surface laplacian and applications to EEG
- http://www.tandfonline.com/doi/abs/10.1080/10790268.2017.1369215
    - [4]: **"Prediction of specific hand movements using EEG signals"**
    - Approach 2 for Phase 3
- https://www.ncbi.nlm.nih.gov/pubmed/28782865
    - [5]: **"Deep Learning With Convolutional Neural Networks for EEG Decoding and Visualization"**
- https://github.com/neurotechuoft/Data-Repository/
    - [6]: **NeurotechUofT: 9-class motor imagery data collection**
        - See "./eeg/motor-imagery/2018-03-17" for raw data
        - See "./eeg/motor-imagery/notes/2018-03-17.md" for experiment setup
        
## Multithreaded architecture (MTA)
The whole program has two basic functions: collect data from the board, and process it somehow. If this were to be done in a single-threaded application, if one iteration of processing were to take too long, it would block the program from receiving data from the board. Due to this, the program uses a multithreaded architecture, with one thread responsible for collecting data and one thread responsible for processing it.

The MTA uses a variant of the publish-subscribe design pattern. A messaging queue is implemented in the Controller class. Controllable classes **can be controlled** by receiving messages in their Controller, and handing the message however appropriate. A master Controller is responsible for receiving instructions from the user and passing them along to each Controllable.

A BioSignal is a Controllable that can also **update** itself with the latest data sample from the board, and **process** data somehow. During each update cycle, it also calls its **control()** method. The updating and processing will occur on separate threads instantiated in the **main()** function. (Look at the Tagger class for an example of a BioSignal).

**main.py** initates the program, which is controlled from the GUI. It first sets up the OpenBCI board, makes the GUI, and then sets up a thread for processing. The GUI then handles playing / pausing the board by instantiating a thread to run **stream()** from openbci_v3. This function streams biosignals from the OpenBCI board, and calls each BioSignals's **update()** function). Processing of BioSignals is handled in **process_thread** (which runs **run_processor()**) by asynchronously calling each BioSignal's process function.


## Plan
![Plan](Meetings/resources/2017-07-17.png?raw=true "Plan")
