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

#run moviefunc


from moviefunc import *
bigset = {'links':[],'movie':[],'cert':[],'rateoc':[],'rateou':[],'release':[],'revcount':[]}
rev = {'name':[],'rate':[],'revi':[],'linkr':[]}
newcheck(bigset,rev)

#import example datasets
revdf = pd.read_csv("rev.csv") #,sep="\\t")
bigdf = pd.read_csv("big.csv") #,sep="\\t")

#keep only reviewers with 10+ reviews
revdf2 = revdf.dropna()
names = revdf2.value_counts(subset = ['name'])
revdfnames = revdf[revdf['name'].isin(names[names>9].reset_index().name)]
revs = revdfnames.value_counts(subset = ['revi'])
revdfrevs = revdfnames[revdfnames['revi'].isin(revs[revs>9].reset_index().revi)]
revmin = revs[revs>9].reset_index().revi
namemin = names[names>9].reset_index().name
revdd= revdfrevs.drop(columns = ['Unnamed: 0','linkr'])


#ignore this bit, it's very ugly and needs to be fixed later
for i in range(len(revdd['rate'].to_list())):
    spar[revdd['revi'].to_list()[i]][revdd['name'].to_list()[i]] = revdd['rate'].to_list()[i]
    
spf = spar.astype(pd.SparseDtype("float", np.nan))

revspar  = tf.data.Dataset.from_tensor_slices(spf)