MADE BY ALI RAZZAK FOR 45SYMBOLS PROPOSAL OF 19/20
NO COMMERCIAL USE INTENDED

To be run in Python3, Ubuntu Mint Sarah.

This script reads a list of keywords in the "pathogenslist.txt" file (seperated by "\n") and inputs them into the rcsb.org search engine. It then takes the top 25 hits for each keyword and downloads the fasta sequence for each of those proteins. It scans the sequence for englih words and scores them based on sentiment analysis (as scored in the "sentiment-words-DFE-785960.csv") file. Finally it returns a list of (".txt") files in directories associated to each search term with the respective proteins name, sentiment ("+" positive or "-" negative) in column 1, matched word (column 2), and score (column 3). 

When using remember to:
1. have "sentiment-words-DFE-785960.csv", "words.txt", and "pathogenlist.txt" in same directory as "protein_search_word_sentiment.py" and all in working directory.
2. "pathogenlist.txt" can be edited for other search terms.
3. path to chrome may be different, if so change "note #1" in script.
4. make sure variable dlpath pathed to same directory as files download to be default, change at "note #2" in script

