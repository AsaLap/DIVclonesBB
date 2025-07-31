#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Antoine Laporte 2025

import bioutils

import argparse
import pandas as pd

parser = argparse.ArgumentParser(description='Applying Levenshtein reduction on kmer matrix')
parser.add_argument('--matrix', action="store", dest='matrix', required=True, type=str, help="Matrix of kmer frequencies, TSV file with first row as line names and kmer as index")
parser.add_argument('--gc_percentage', action="store", dest='gc_percentage', type=float, default=None, help="Percentage of GC content of the kmer matrix")
parser.add_argument('--len_kmer', action="store", dest='len_kmer', type=int, default=21, help="Length of kmers")
parser.add_argument('--p_value', action="store", dest='p_value', type=float, default=0.05, help="Threshold P-value to select kmers")
parser.add_argument('--eco_mode', action="store", dest='eco_mode', type=bool, default=True, help="Eco mode, restrains the gathering of data on python dataframe, toggle on for debugging on small datasets")
parser.add_argument('--remove_specific', action='store', dest='remove_specific', type=bool, default=False, help="Remove specific kmer from matrix")


args = parser.parse_args()

# --- 0. Print info of run in the log file
print("Matrix : ", args.matrix)
print("Specific removed : ", args.remove_specific)

# --- 1. Loading data
matrix = pd.read_csv(args.matrix, sep='\t', header=0, index_col=0)

# --- 2. Removing line-specific kmers
if args.remove_specific:
    matrix = bioutils.remove_specific(matrix)

# --- 3. Getting a list of kmer to keep, according to Levenshtein selection
list_kmer = matrix.index.tolist()
if args.eco_mode:
    list_selected_kmer = bioutils.levenshtein_kmer_selection(list_kmer,
                                                             gc_percentage=args.gc_percentage,
                                                             len_kmer=args.len_kmer,
                                                             p_value=args.p_value,
                                                             eco_mode=args.eco_mode)
else:
    list_selected_kmer, list_unselected_kmer, dict_kmer = bioutils.levenshtein_kmer_selection(list_kmer,
                                                                                              gc_percentage=args.gc_percentage,
                                                                                              len_kmer=args.len_kmer,
                                                                                              p_value=args.p_value,
                                                                                              eco_mode=args.eco_mode)

# --- 4. Checking list differences
print("Selected kmer list length :", len(list_selected_kmer))
print("Original kmer list length :", len(list_kmer))
print('= Reduction of%5.1f percent' % float(100-(len(list_selected_kmer)/len(list_kmer)*100)))

# --- 5. Creating and saving new dataset
matrix_levenshtein = matrix.loc[list_selected_kmer]
matrix_levenshtein.to_csv(args.matrix.split(".")[0] + '_levenshtein.tsv', sep='\t')
