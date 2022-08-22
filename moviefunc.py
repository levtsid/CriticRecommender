import time,random,os,sys,re,glob
import numpy as np
from bs4 import BeautifulSoup
import pandas as pd
import requests
from random import randint

headers_a = {'User-Agent': 'Mozilla/5.0' }

#bigset = {'links':[],'movie':[],'cert':[],'rateoc':[],'rateou':[]}

def newcheck(pile,out): #test for new additions to database
    for i in range(0,1):
        url="https://www.metacritic.com/browse/movies/score/metascore/all/filtered?view=detailed&page=%d" %(i)
        headers_a = {'User-Agent': 'Mozilla/5.0' }
        resp = requests.get(url,headers = headers_a)
        htmlpile = BeautifulSoup(resp.text, 'html.parser')
        for name1 in htmlpile.find_all('tr'):
            if not name1.find('td'):
                continue
            if name1.find('a', class_='title').attrs['href'].split('/movie/')[1] in pile['links']:
                continue
            pile['links'].append(name1.find('a', class_='title').attrs['href'].split('/movie/')[1])
            pile['movie'].append(name1.find('h3').text)
            if len(name1.select('div.clamp-details')[0].text.split('|')) > 1:
                pile['cert'].append(name1.select('div.clamp-details')[0].text.split('|')[1].strip())
            else:
                pile['cert'].append('Not Rated')
            pile['rateoc'].append(name1.find('div', class_=re.compile('metascore_w large*')).text)
            pile['rateou'].append(name1.find('div', class_=re.compile('metascore_w user*')).text)
            pile['revcount'].append(0)
            mov = len(pile['links'])-1
            revadd(pile,out,mov)
        time.sleep(randint(3,20))
        
    
    
#rev = {'name':[],'rate':[],'revi':[],'linkr':[]}
def revadd(pile,out,mov): #add reviews
    #for i in range(0,1): #range(len(pile['links'])):
    #revcount = 0
    url2="https://www.metacritic.com/movie/%s/critic-reviews" %(pile['links'][mov])
    resp = requests.get(url2,headers = headers_a)
    pagec = BeautifulSoup(resp.text, 'html.parser')
    #print (pagec.find('span', class_='based_on'))
    if not pagec.find('span', class_='based_on'):
        return
    else:
        pages = pagec.find('span', class_='based_on').text.split()
    pageq = -1 * (-int(pages[2]) // 100)
    for j in range(0,pageq):
        pagetest(mov,j,pile,out)
#           resp = requests.get(url2,headers = headers_a)
#            revpile = BeautifulSoup(resp.text, 'html.parser')
#            for review in revpile.find_all('div', class_=re.compile('review*')):
#                if not review.find('span', class_='author') or re.match("Staff \(No[tn] Credited\)", review.find('span', class_='author').text) :
#                    continue
#                if j > 0 and revcount < 100:
#                    break
#                elif j > 0 and rev['name'][i-100] == review.find('span', class_='author').find('a').text:
#                    break
#                #print (review)
#                rev['revi'].append(bigset['movie'][i])
#                if review.find('span', class_='author').find('a'):
#                    rev['linkr'].append(review.find('span', class_='author').find('a').attrs['href'].split('/critic/')[1].split('?')[0])
#                    rev['name'].append(review.find('span', class_='author').find('a').text)
#                else:
#                    rev['name'].append(review.find('span', class_='author').text)
#                    rev['linkr'].append(review.find('span',class_='author').text)
#                rev['rate'].append(review.find('div', class_=re.compile('metascore_w*')).text)
#                revcount = revcount + 1
#            sleep(randint(3,20))

def pagetest(mov,num,pile,out): #test for additional reviews
    url2="https://www.metacritic.com/movie/%s/critic-reviews?page=%d" %(pile['links'][mov], num)
    resp = requests.get(url2,headers = headers_a)
    revpile = BeautifulSoup(resp.text, 'html.parser')
    for review in revpile.find_all('div', class_=re.compile('review*')):
        if not review.find('span', class_='author') or re.match("Staff \(No[tn] Credited\)", review.find('span', class_='author').text) :
            continue
        if num > 0 and pile['revcount'] < num*100:
            return
        #elif num > 0 and out['name'][mov-100] == review.find('span', class_='author').find('a').text:
        #    return
        out['revi'].append(pile['movie'][num])
        if review.find('span', class_='author').find('a'):
            out['linkr'].append(review.find('span', class_='author').find('a').attrs['href'].split('/critic/')[1].split('?')[0])
            out['name'].append(review.find('span', class_='author').find('a').text)
        else:
            out['name'].append(review.find('span', class_='author').text)
            out['linkr'].append(review.find('span',class_='author').text)
        out['rate'].append(review.find('div', class_=re.compile('metascore_w*')).text)
        pile['revcount'][num] = pile['revcount'][num] + 1
    time.sleep(randint(3,20))