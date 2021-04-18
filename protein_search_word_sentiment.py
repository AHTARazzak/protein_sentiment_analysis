from requests_html import HTMLSession
import urllib.request, urllib.error, urllib.parse
import webbrowser
from bs4 import BeautifulSoup
import pyautogui
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.support.ui import WebDriverWait
import re
import enchant
import shutil
import pandas as pd
from statistics import mean 
import os
import sys

dlfilepath=str(sys.argv[1])
scriptpath=str(sys.argv[2])

# Read in sentiment analysis data
sentimentana=pd.read_csv("sentiment-words-DFE-785960.csv")
positivesentiment = sentimentana[['q1_identify_the_term_that_is_associated_with_the_most_amount_of_positive_sentiment_or_least_amount_of_negative_sentiment','q1_identify_the_term_that_is_associated_with_the_most_amount_of_positive_sentiment_or_least_amount_of_negative_sentiment:confidence']]
negativesentiment = sentimentana[['q2_identify_the_term_that_is_associated_with_the_most_amount_of_negative_sentiment_or_least_amount_of_positive_sentiment','q2_identify_the_term_that_is_associated_with_the_most_amount_of_negative_sentiment_or_least_amount_of_positive_sentiment:confidence']]

# Make list of english words.
wordlist=[]
words = set(x for x in open("words.txt").readlines())
for i in words:
    strpi = i.strip()
    if strpi.islower():
        if strpi.isalnum():
            if len(i) > 1:
                wordlist.append(strpi)
				
# Read pathogen list
withpatho = []
with open("pathogenlist.txt") as dis:
    for line in dis:
        if len(line) > 1:
            wordtrim = line.strip()
            searchword = wordtrim.replace(" ","%20")
            withpatho.append(searchword)

for qpatho in withpatho:
    pathogen = qpatho
    path = os.path.join(os.getcwd(), pathogen) 
    os.mkdir(path) 
    #url path for protein data base search engine, dependency on Chrome
    url = 'https://www.rcsb.org/search?request=%7B%22query%22%3A%7B%22parameters%22%3A%7B%22value%22%3A%22'+pathogen+'%22%7D%2C%22type%22%3A%22terminal%22%2C%22service%22%3A%22text%22%2C%22node_id%22%3A0%7D%2C%22return_type%22%3A%22entry%22%2C%22request_options%22%3A%7B%22pager%22%3A%7B%22start%22%3A0%2C%22rows%22%3A100%7D%2C%22scoring_strategy%22%3A%22combined%22%2C%22sort%22%3A%5B%7B%22sort_by%22%3A%22score%22%2C%22direction%22%3A%22desc%22%7D%5D%7D%2C%22request_info%22%3A%7B%22src%22%3A%22ui%22%2C%22query_id%22%3A%224fd19d7ad36839f52b83a7f42c4a6437%22%7D%7D'
	chrome_path = '/usr/bin/google-chrome %s'
    webbrowser.get(chrome_path).open(url)
    # Need to slow down scrapping to avoid 403
    time.sleep(5)
    pyautogui.hotkey('ctrl', 's')
    time.sleep(1)
    pyautogui.typewrite(pathogen+"page")
    pyautogui.hotkey('enter')
    time.sleep(8)
    # Move around directories, need to specific for user
    shutil.move(dlfilepath + "/" + pathogen + "page.html", path+"/" + pathogen + "page.html")
    f = open(scriptpath + '/' + pathogen+"/" + pathogen + "page.html", "r")
    f = open(path + "/" + pathogen + "page.html", "r")
    soup = BeautifulSoup(f, 'lxml')
    pdblinks = soup.find_all("a", href = True)
    # Collect all PDB hits
    links = []
    for a in pdblinks:
        links.append(a['href'])
    onlystructure = []
    for l in links:
        if 'structure' in l:
            onlystructure.append(l)
    def unique(list1): 
        unique_list = [] 
        for x in list1: 
            if x not in unique_list: 
                unique_list.append(x)
        return unique_list
    onlypdb = []
    for i in unique(onlystructure):
        onlypdb.append(i[-4:])
    print(onlypdb)
    for i in onlypdb:
        webbrowser.get(chrome_path).open('https://www.rcsb.org/fasta/entry/' + str(i))
        time.sleep(2)
        shutil.move(dlfilepath + "/rcsb_pdb_" + str(i) + ".fasta", path + "/rcsb_pdb_" + str(i) + ".fasta")
    for i in onlypdb:   
        pdb = i
        p = open(path+"/rcsb_pdb_" + str(i) + ".fasta", "r")
        linecount = 0
        for line in p:
            if ">" not in line:
                code = line.split('\n')[0]
        lowcode = (code.lower())
        pdbcodewords = []
        for i in wordlist:
            if i in lowcode:
                pdbcodewords.append(i)
        realwords = []
        d = enchant.Dict("en_US")
        for i in pdbcodewords:
            if d.check(i):
                realwords.append(i)
        hitlist = []
        for i in realwords:
            sentimentscorepos = positivesentiment[positivesentiment.columns[0]].eq(i)
            trumatchindex = sentimentscorepos.index[sentimentscorepos == True].tolist()
            if (len(trumatchindex) > 0):
                thescorespos = positivesentiment.iloc[trumatchindex, 1 ].tolist()
                hitlist.append("+ " + (i) + " " + str(mean(thescorespos)))
            sentimentscoreneg = negativesentiment[negativesentiment.columns[0]].eq(i)
            negmatchindex = sentimentscoreneg.index[sentimentscoreneg == True].tolist()
            if (len(negmatchindex) > 0):
                thescoresneg = negativesentiment.iloc[negmatchindex, 1 ].tolist()
                hitlist.append("- " + (i) + " " + str(mean(thescoresneg)))
        thescorefile = pdb + pathogen + "wordscore.txt"
        with open(thescorefile, "w+") as f:
            f.write(str(len(hitlist)) + "\n")
            for i in hitlist:
                f.write(i + "\n")
        f.close()
        path = os.path.join(os.getcwd(), pathogen) 
        shutil.move(os.getcwd() + "/" + thescorefile, path + "/" + thescorefile)