import time,random,os,sys,re,glob
import numpy as np
from bs4 import BeautifulSoup
import pandas as pd
import requests
import random

headers_a = {'User-Agent': 'Mozilla/5.0' }

#data formats
#pile = {'links':[],'movie':[],'cert':[],'rateoc':[],'rateou':[],'release':[],'revcount':[]}
#out = {'name':[],'rate':[],'revi':[],'linkr':[]}

def newcheck(pile,out): #test for new additions to database
    url="https://www.metacritic.com/browse/movies/score/metascore/all/filtered?view=detailed"
    resp = requests.get(url,headers = headers_a)
    htmlpile = BeautifulSoup(resp.text, 'html.parser')
    pags = htmlpile.find('li',class_='page last_page').find('a').text
    for i in range(0,int(pags)):
        url="https://www.metacritic.com/browse/movies/score/metascore/all/filtered?view=detailed&page=%d" %(i)
        resp = requests.get(url,headers = headers_a)
        htmlpile = BeautifulSoup(resp.text, 'html.parser')
        for name1 in htmlpile.find_all('tr'):#add movies in fields
            urlm="https://www.metacritic.com/movie/%s/" %(pile['links'][mov])
            resp1 = requests.get(urlm,headers = headers_a)
            page2 = BeautifulSoup(resp1.text, 'html.parser')
            if not blah:
                links
            else:
                links
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
        time.sleep(random.random())
        
    
    

def revadd(pile,out,mov): #add reviews
    url2="https://www.metacritic.com/movie/%s/critic-reviews" %(pile['links'][mov])
    resp = requests.get(url2,headers = headers_a)
    pagec = BeautifulSoup(resp.text, 'html.parser')
    if not pagec.find('span', class_='based_on'):#check the review quantity
        return
    else:
        pages = pagec.find('span', class_='based_on').text.split()
    pageq = -1 * (-int(pages[2]) // 100)
    for j in range(0,pageq):
        pagetest(mov,j,pile,out)


def pagetest(mov,num,pile,out): #test for additional reviews
    url2="https://www.metacritic.com/movie/%s/critic-reviews?page=%d" %(pile['links'][mov], num)
    resp = requests.get(url2,headers = headers_a)
    revpile = BeautifulSoup(resp.text, 'html.parser')
    for review in revpile.find_all('div', class_=re.compile('review*')):
        if not review.find('span', class_='author') or re.match("Staff \(No[tn] Credited\)", review.find('span', class_='author').text) : #ignore no author
            continue
        if review.find('span', class_='author').text in out['name']: #skip existing
            continue
        if num > 0 and pile['revcount'] < num*100: #page check
            return
        elif num > 0 and out['name'][mov-100] == review.find('span', class_='author').find('a').text:
            return
        out['revi'].append(pile['movie'][mov])
        if review.find('span', class_='author').find('a'): #ingest review
            out['linkr'].append(review.find('span', class_='author').find('a').attrs['href'].split('/critic/')[1].split('?')[0])
            out['name'].append(review.find('span', class_='author').find('a').text)
        else:
            out['name'].append(review.find('span', class_='author').text)
            out['linkr'].append(review.find('span',class_='author').text)
        out['rate'].append(review.find('div', class_=re.compile('metascore_w*')).text)
        pile['revcount'][mov] = pile['revcount'][mov] + 1
    time.sleep(random.random())