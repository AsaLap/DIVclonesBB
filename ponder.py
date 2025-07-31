#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Antoine Laporte 2025
# with help from Gauthier Sarah

import argparse
import pandas as pd
from io import StringIO
from scipy.stats import chisquare

parser = argparse.ArgumentParser(description='Applying Levenshtein selection and depth pondering on kmer matrix')
parser.add_argument('--matrix', action="store", dest='matrix', required=True, type=str, help="Matrix of kmer frequencies, TSV file with first row as line names and kmer as index")
parser.add_argument('--sep', action="store", dest='sep', type=str, default="\t", help="Separator between columns in matrix")
#---Pondering arguments---#
parser.add_argument('--names', action="store", dest='names', required=True, help="Names of lines in same order as they are in the matrix, each name on a new line type file")
parser.add_argument('--coverage', action="store", dest='coverage', required=True, help="Mean coverage value for each line with 'Line' and 'Coverage' headers, TSV file")
parser.add_argument('--round', action="store", dest='round', default=2, help="Rounding number of the matrix")

args = parser.parse_args()

# --- 0. Print info of run in the log file
print("Matrix : ", args.matrix)
print("round : ", args.round)

# --- 1. Load line names from provided lst file
with open(args.names, 'r') as f:
    noms_colonnes = [ligne.strip() for ligne in f]

# --- 2. Import coverage values dataframe
nb_reads = pd.read_csv(args.coverage, sep='\t')
nb_reads['line'] =  nb_reads['line_fr'].apply(lambda x:  str(x).split("_R")[0]) # getting line names only
nb_reads = nb_reads.groupby('line').sum() # suming all lines to get R1 and R2 on the same line, line is now index
nb_reads["coverage"] = nb_reads["nb_reads"] * 150 / 500000000 # applying nb reads * 150 (size of a read) / 500 000 000 (size of genome)
nb_reads.to_csv(args.coverage.split(".")[0] + '_coverage.tsv', sep="\t")
print("Coverage dataframe : ", "\n", nb_reads)
df_division = nb_reads["coverage"].reset_index(drop=True)
df_division.index += 1 #set index from 1 to match index from next matrix

# --- 3. Loop to ponder number of kmer by coverage
count_kmer = 0
count_selected_kmer = 0
with open(args.matrix, "r") as file:
    for line in file:
        count_kmer+=1
        kmer_line = pd.read_csv(StringIO(line), sep=args.sep, index_col=0, header=None)
        kmer = str(kmer_line.iloc[0].name)
        #ponder
        kmer_line = kmer_line.T.div(df_division, axis=0).round(args.round).T
        #write
        kmer_line.to_csv(args.matrix.split(".")[0] + '_pondered.tsv', sep="\t", header=False, mode='a')