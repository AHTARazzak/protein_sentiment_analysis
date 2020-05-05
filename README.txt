ALI RAZZAK SCRIPT PRODCUED FOR 45 SYMBOLS PROJECT SUBMISSION
NOT COMMERCIAL USE INTENDED

README for "PDBscrape_protein_sentiment_analysis.py"

This script reads a list of words in a file ("pathogenlist.txt), searches proteins related to the each word in the protein databae (rcsb.org), downloads fasta files related to the top 25 proteins related to the word, scans the amino acid sequence of the fasta file for words and scores the wods sentiment according to sentiment analysis (as determined by "sentiment-words-DFE-785960.csv"). It then returns a file relating to each protein that contains the protein name, sentiment "+" (positive) or "-" (negative) column 1, the word in column 2, and the score in column 3. The files are organised into directories according to the search them, each directory contains a file for the fasta sequence and a file for the sequence score.

the script takes two inputs: 
1) the path to where files default download to
2) the path where the script itself is

The search uses chrome, ensure to configure the pathway to your chrome excutable (see "#note 1" in script).

Scriptflow
1. Search rcsb data base for each word in "pathogenlist.txt"
2. Download html page for word search.
3. Make directory in script directory for each pathogen.
4. Read html and download fasta sequence of top 25 proteins.
5. Read fasta file AA sequence of each protein & check for all words in sequence.
6. Find words among word list and score using sentiment analysis, assigning sneitment ("+" or "-" negaive), and score to each word.
7. Organise fasta file and score file into directories relating to each search word.
