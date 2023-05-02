import numpy as np
import scipy as sp
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
import os, re, importlib, requests, time, tempfile, pprint, glob, imageio
import PIL
from typing import Dict, Text
from IPython import display
from bs4 import BeautifulSoup
from IPython.core.display import clear_output
from warnings import warn
from random import randint

import collections
from typing import Dict, List, Optional, Text, Tuple

import tensorflow_ranking as tfr
import tensorflow_recommenders as tfrs

from rankmod import RankingModel

#run moviefunc
from moviefunc import *
bigset = {'links':[],'movie':[],'cert':[],'rateoc':[],'rateou':[],'release':[],'revcount':[]}
rev = {'name':[],'rate':[],'revi':[],'linkr':[]}
newcheck(bigset,rev)

#import example datasets
revdf = pd.read_csv("rev.csv") #,sep="\\t")
bigdf = pd.read_csv("big.csv") #,sep="\\t")

#keep only reviewers with 10+ reviews, and movies with 10+ reviews
revdf2 = revdf.dropna()

names = revdf2.value_counts(subset = ['name'])
revdfnames = revdf[revdf['name'].isin(names[names>9].reset_index().name)]

revs = revdfnames.value_counts(subset = ['revi'])
revdfrevs = revdfnames[revdfnames['revi'].isin(revs[revs>9].reset_index().revi)]

revdd= revdfrevs.drop(columns = ['Unnamed: 0','linkr'])

revmin = revs[revs>9].reset_index().revi
namemin = names[names>9].reset_index().name


#ignore this bit, it's very ugly and needs to be fixed later
for i in range(len(revdd['rate'].to_list())):
    spar[revdd['revi'].to_list()[i]][revdd['name'].to_list()[i]] = revdd['rate'].to_list()[i]
    
#replacement code for ugly loop
index=list(revmin)
columns=list(namemin)
index=sorted(index)
columns=sorted(columns)
 
util_df=pd.pivot_table(data=revdd,values='rate',index='name',columns='revi')    

#convert dataframe to dataset of tensor slices
spf = spar.astype(pd.SparseDtype("float", np.nan))

#only needed for initial matrix tensor, not currently in use
#revspar  = tf.data.Dataset.from_tensor_slices(spf)

#add id and title data to each set
tensor_slic = {"user_id": [], "movie_title": [], "user_rating": []}

tensor_slic["user_rating"] = spf.to_dict('split')['data']
tensor_slic["user_id"] = spf.index
tensor_slic["movie_title"] = [spf.columns]*len(namemin)
    
tfda = tf.data.Dataset.from_tensor_slices(tensor_slic)


#batch and separate test and train data
testlen=600
bsize=25
epo=50
trtf = tfda.take(testlen)
tetf = tfda.skip(testlen).take(len(namemin)-testlen)
cached_tfr = trtf.shuffle(testlen).batch(bsize).cache()
cached_tfe = tetf.batch(bsize).cache()

#compute fit and test
listwise_model = RankingModel(tfr.keras.losses.ListMLELoss())
listwise_model.compile(optimizer=tf.keras.optimizers.Adagrad(0.1))


listwise_model.fit(cached_tfr, epochs=epo, verbose=True)
#test with validation data set
listwise_model_result = listwise_model.evaluate(cached_tfe, return_dict=True)
