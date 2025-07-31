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
#---Levenshtein P1 arguments---#
parser.add_argument('--len_kmer', action="store", dest='len_kmer', type=int, default=21, help="Length of kmers")

args = parser.parse_args()

# --- 0. Print info of run in the log file
print("Matrix : ", args.matrix)
print("len_kmer : ", args.len_kmer)

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

