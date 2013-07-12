#! /usr/bin/python

'''
salientAudio.py
Miles Thorogood
mthorogo@sfu.ca
last modified July 2013

Program to predict the valence and arousal of 4 second audio chunks.
It uses a standard mlr algorithm trained with data derived from human subject study
If your wanting to supply your own training set then pay attention to the feature 
extraction technique that can be gleened from the process method and the yaafeEngine. 
If you need assistance in creating such a training set you can ontact the author by email

Input:
    wav or aiff audio file >= 4seconds
Output:
    csv file with valence, arousal, start time, end time
     
Usage:
    python salientAudio.py path/to/audio/file.wav(aif)

    
Dependencies:
    feature extraction http://yaafe.sourceforge.net/
    OLS algorithm      http://wiki.scipy.org/Cookbook/OLS
    yaafeEngine.py and salientTraining.csv (should be with the repo)
'''

import sys
import csv
import numpy as np
from math import floor, sqrt
from yaafeEngine import yaafengine       
import ols


class MLRmodel:
    
    # yData is a 1xn numpy matrix. xData is a kxn numpy matrix
    def __init__(self, y, x, ylabel, xlabels):
        self.model = ols.ols(y,x,ylabel,xlabels)
        self.coefficients = self.model.b
        self.model.summary() 
        
    def predict(self, data):
        print data
        return sum(self.coefficients*data) # typical mlr b0 + b1*x1 + b2*x2 + ... + bn*xn
           
class audio_affect:
    
    # tFile is a csv file
    # pleasantResponse, eventfulResponse, Loud_Mean,Loud_Std,MFCC1_Mean,MFCC1_Std,MFCC2_Mean,MFCC2_Std,MFCC3_Mean,MFCC3_Std
    def __init__(self, tFile):
        
        data = []
        with open(tFile, 'rb') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',')
            firstrow = True
            for row in csvreader:
                if firstrow: firstrow = False
                else:
                    data.append([float(i) for i in row])
        data = np.array(data)  
        print data[:,2:].shape
        explanitories = ['loud mean', 'loud std', 'mfcc1 mean', 'mfcc1 std', 'mfcc2 mean', 'mfcc2 std', 'mfcc3 mean', 'mfcc3 std']
        self.pleasantModel = MLRmodel(data[:,0], data[:,2:], 'valence', explanitories) ;
        self.eventfulModel = MLRmodel(data[:,1], data[:,2:], 'arousal', explanitories) ;

        # the following properties should be the same as the training data extraction
        self.window_size = 4 # analysis window in seconds
        self.sRate = 22500 # sample rate 
        self.nframes = 512 # yaafe feature block block size
        self.yengine = yaafengine(self.sRate, self.nframes)

	
	# audio file path
    def process(self, afile):
        fvecs = self.yengine.featureVectors(afile)
        # calculate the length of analysis blocks
        block_duration = float(self.nframes/2)/float(self.sRate) # time duration of an analysis block
        num_blocks_in_window = int(floor(self.window_size / block_duration)) # number of blocks in our analysis window
        print "total blocks = " + str(len(fvecs)) + ". num blocks in window = " + str(num_blocks_in_window)
        processed = []
        # scan across by window length
        for i in xrange(0, len(fvecs), num_blocks_in_window):
            window = fvecs[i:i+num_blocks_in_window] # get the vectors for the window
            accum = zip(*window)
            features = [1]
            # Do the bag of frames
            for cc in accum: # go through each dimension
                n = len(cc)
                mean = sum(cc)/n
                std = sqrt(sum((x-mean)**2 for x in cc) / n)
                mvalue = mean
                features.append(mvalue)
                svalue = std
                features.append(svalue)
            # predict
            pleasantPredict = self.pleasantModel.predict(np.array(features))
            eventfulPredict = self.eventfulModel.predict(np.array(features))
            start_time =float(i*(self.nframes/2))/float(self.sRate) # Assumes overlapping
            end_time =float((i+num_blocks_in_window)*(self.nframes/2))/float(self.sRate)
            processed.append({'valence':pleasantPredict, 'arousal':eventfulPredict, 'start':start_time, 'end':end_time})

        with open(afile+'_salient.csv', 'wb') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',')
            csvwriter.writerow(['valence', 'arousal', 'start', 'end'])
            for dic in processed:
                csvwriter.writerow([dic['valence'], dic['arousal'], dic['start'], dic['end']])
                
            

def main():
    predictioner = audio_affect('salientTraining.csv')
    predictioner.process(sys.argv[1]) # this will be the audio file
    
if __name__ == "__main__":
    main()
            
            
            
            
            