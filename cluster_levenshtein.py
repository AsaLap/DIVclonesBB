#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Antoine Laporte 2025

import bioutils

import argparse
import pandas as pd

parser = argparse.ArgumentParser(description='Applying Levenshtein reduction on kmer matrix')
parser.add_argument('--matrix', action="store", dest='matrix', required=True, type=str, help="Matrix of kmer frequencies, TSV file with first row as line names and kmer as index")
parser.add_argument('--remove_specific', action='store', dest='remove_specific', type=bool, default=False, help="Remove specific kmer from matrix")
parser.add_argument('--a_percentage', action="store", dest='a_percentage', type=float, default=32.5, help="Percentages of A, T, C and G of the reference genome")
parser.add_argument('--t_percentage', action="store", dest='t_percentage', type=float, default=32.5, help="Percentages of A, T, C and G of the reference genome")
parser.add_argument('--c_percentage', action="store", dest='c_percentage', type=float, default=17.5, help="Percentages of A, T, C and G of the reference genome")
parser.add_argument('--g_percentage', action="store", dest='g_percentage', type=float, default=17.5, help="Percentages of A, T, C and G of the reference genome")
parser.add_argument('--sep', action="store", dest='sep', type=str, default="\t", help="Separator between columns in matrix")
parser.add_argument('--len_kmer', action="store", dest='len_kmer', type=int, default=21, help="Length of kmers")
parser.add_argument('--p_value', action="store", dest='p_value', type=float, default=0.05, help="Threshold P-value to select kmers")


args = parser.parse_args()

# --- 0. Print info of run in the log file
print("Matrix : ", args.matrix)
print("Specific removed : ", args.remove_specific)

# --- 1. Loading data
matrix = pd.read_csv(args.matrix, sep=args.sep, header=0, index_col=0, engine='python')

# --- 2. Removing line-specific kmers
if args.remove_specific:
    matrix = bioutils.remove_specific(matrix)

# --- 3. Getting a list of kmer to keep, according to Levenshtein selection
list_kmer = matrix.index.tolist()
atcg_percentage = {"a": args.a_percentage,
                   "t": args.t_percentage,
                   "c": args.c_percentage,
                   "g": args.g_percentage}
list_selected_kmer = bioutils.levenshtein_select(list_kmer,
                                                 atcg_per=atcg_percentage,
                                                 len_kmer=args.len_kmer,
                                                 p_value=args.p_value)

# --- 4. Checking list differences
print("Selected kmer list length :", len(list_selected_kmer))
print("Original kmer list length :", len(list_kmer))
print('= Reduction of%5.1f percent' % float(100-(len(list_selected_kmer)/len(list_kmer)*100)))

# --- 5. Creating and saving new dataset
matrix_levenshtein = matrix.loc[list_selected_kmer]
matrix_levenshtein.to_csv(args.matrix.split(".")[0] + '_levenshtein.tsv', sep='\t')
