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
#---Levenshtein arguments---#
# parser.add_argument('--header', action="store", dest='header', type=str, default=None, help="0 if matrix has a header (pondered matrix for instance)")
parser.add_argument('--gc_percentage', action="store", dest='gc_percentage', type=float, default=None, help="Percentage of GC content of the kmer matrix")
parser.add_argument('--len_kmer', action="store", dest='len_kmer', type=int, default=21, help="Length of kmers")
parser.add_argument('--p_value', action="store", dest='p_value', type=float, default=0.05, help="Threshold P-value to select kmers")
parser.add_argument('--remove_specific', action='store', dest='remove_specific', type=bool, default=False, help="Remove specific kmer from matrix")
#---Pondering arguments---#
parser.add_argument('--names', action="store", dest='names', required=True, help="Names of lines in same order as they are in the matrix, each name on a new line type file")
parser.add_argument('--coverage', action="store", dest='coverage', required=True, help="Mean coverage value for each line with 'Line' and 'Coverage' headers, TSV file")
parser.add_argument('--round', action="store", dest='round', default=2, help="Rounding number of the matrix")

args = parser.parse_args()

# --- 0. Print info of run in the log file
print("Matrix : ", args.matrix)
print("Specific removed : ", args.remove_specific)
print("gc_percentage : ", args.gc_percentage)
print("len_kmer : ", args.len_kmer)
print("p_value : ", args.p_value)
print("round : ", args.round)

# --- 1. First loop to get GC and TA values
c_count = 0
g_count = 0
t_count = 0
a_count = 0
count_all_bases = 0
with open(args.matrix, 'r') as file:
    for line in file:
        kmer_line = pd.read_csv(StringIO(line), sep=args.sep, index_col=0, header=None)
        kmer = str(kmer_line.iloc[0].name)
        c_count += kmer.count("C")
        g_count += kmer.count("G")
        t_count += kmer.count("T")
        a_count += kmer.count("A")
        count_all_bases += 21

#--- 2. Calculation of expected values for the selection
c_proportion = c_count / count_all_bases
g_proportion = g_count / count_all_bases
t_proportion = t_count / count_all_bases
a_proportion = a_count / count_all_bases
g_expected = c_expected = (g_proportion + c_proportion) * args.len_kmer / 2
t_expected = a_expected = (t_proportion + a_proportion) * args.len_kmer / 2
print("G expected by kmer (calculated from kmer) :", g_expected)
print("C expected by kmer (calculated from kmer) :", c_expected)
print("T expected by kmer (calculated from kmer) :", t_expected)
print("A expected by kmer (calculated from kmer) :", a_expected)

# --- 3. Load line names from provided lst file
with open(args.names, 'r') as f:
    noms_colonnes = [ligne.strip() for ligne in f]

# --- 5. Import coverage values dataframe
nb_reads = pd.read_csv(args.coverage, sep='\t')
nb_reads['line'] =  nb_reads['line_fr'].apply(lambda x:  str(x).split("_R")[0]) # getting line names only
nb_reads = nb_reads.groupby('line').sum() # suming all lines to get R1 and R2 on the same line, line is now index
nb_reads["coverage"] = nb_reads["nb_reads"] * 150 / 500000000 # applying nb reads * 150 (size of a read) / 500 000 000 (size of genome)
nb_reads.to_csv(args.coverage.split(".")[0] + '_coverage.tsv', sep="\t")
print("Coverage dataframe : ", "\n", nb_reads)
df_division = nb_reads["coverage"].reset_index(drop=True)
df_division.index += 1 #set index from 1 to match index from next matrix

# --- 4. Second loop to ponder number of kmer by coverage and select kmer by the levenshtein method
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
        c_obs = kmer.count("C")
        g_obs = kmer.count("G")
        t_obs = kmer.count("T")
        a_obs = kmer.count("A")
        chi = chisquare([g_obs, c_obs, t_obs, a_obs], f_exp=[g_expected, c_expected, t_expected, a_expected])
        if chi.pvalue > args.p_value: # take those who are dependent and do not respect H0 hypothesis of independence
            count_selected_kmer+=1
            kmer_line.to_csv(args.matrix.split(".")[0] + '_pondered_levenshtein.tsv', sep="\t", header=False, mode='a')

# --- 5. Checking list differences
print("Selected kmer list length :", count_selected_kmer)
print("Original kmer list length :", count_kmer)
print('= Reduction of%5.1f percent' % float(100-(count_selected_kmer/count_kmer*100)))