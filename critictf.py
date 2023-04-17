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