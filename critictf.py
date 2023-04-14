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