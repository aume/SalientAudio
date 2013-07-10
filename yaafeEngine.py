#! /usr/bin/python

'''
yaafeEngine.py
requires the excellent audio feature extraction software from http://yaafe.sourceforge.net/
Miles Thorogood
mthorogo@sfu.ca
2013
'''


import os
import sys
from math import sqrt


from yaafelib import *



class yaafengine:
    def __init__(self, srate, bsize):
        #FeaturePlan is a collection of features to extract, configured for a specific sample rate.
        fp = FeaturePlan(sample_rate=srate, resample=True)

        blocksize = bsize
        step = bsize/2
        fp.addFeature('MFCC: MFCC CepsNbCoeffs=3 blockSize=%d stepSize=%d' % (blocksize, step))
        fp.addFeature('Loudness: Loudness LMode=Total blockSize=%d stepSize=%d' % (blocksize, step))
        # x fp.addFeature('PerceptualSharpness: PerceptualSharpness blockSize=%d stepSize=%d' % (blocksize, step))
        # x fp.addFeature('PerceptualSpread: PerceptualSpread blockSize=%d stepSize=%d' % (blocksize, step))
        #fp.addFeature('PerceptualFlatnes: PerceptualFlatnes blockSize=%d stepSize=%d' % (blocksize, step))
        
        # A DataFlow object hold a directed acyclic graph of computational steps describing how to compute some audio features.
        df = fp.getDataFlow()
        # A Engine object is in charge of processing computations defined in a DataFlow object on given inputs
        self.engine = Engine()
        self.engine.load(df)
        # go and process all our files in the dictionaries
        self.afp = AudioFileProcessor()

    # runs the yaafe extraction
    def extractFeatures(self, file):
        self.afp.processFile(self.engine, file) # extract features from an audio file using AudioFileProcessor
        feats = self.engine.readAllOutputs()
        return feats

    # returns an array of feature vectors
    def featureVectors(self, file, nump=False):
        feats = self.extractFeatures(file)
        flist =[]
        fnames = [] # The features order
        for feat in feats:
            fnames.append(feat)
            if not nump: flist.append(feats[feat].tolist())
            else: flist.append(feats[feat])
        flist = zip(*flist)
        fvecs = []
        for f in flist:
    		fvecs.append([j for i in f for j in i])
        return fvecs
		
