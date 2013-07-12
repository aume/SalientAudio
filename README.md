SalientAudio
============

salientAudio.py
mthorogo at sfu dot ca
last modified July 2013

Todo:
-----
implement pre-processing stage to normalize variables

About:
------
Program to predict the valence and arousal of 4 second audio chunks.
Algorithm pulled from http://nime2013.kaist.ac.kr/program/papers/day2/poster2/157/157_Paper.pdf

It uses a standard mlr algorithm trained with data derived from human subject study
If your wanting to supply your own training set then pay attention to the feature 
extraction technique that can be gleened from the process method and the yaafeEngine. 
If you need assistance in creating such a training set you can ontact the author by email

Input:  wav or aiff audio file >= 4seconds
Output: csv file with valence, arousal, start time, end time
     
Usage: 
-----
python salientAudio.py path/to/audio/file.wav(aif)
    
Dependencies:
--------------
    feature extraction http://yaafe.sourceforge.net/
    
    OLS algorithm      http://wiki.scipy.org/Cookbook/OLS
    
    yaafeEngine.py and salientTraining.csv (should be with the repo)
