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
parser.add_argument('--gc_percentage', action="store", dest='gc_percentage', type=float, default=None, help="Percentage of GC content of the kmer matrix")
parser.add_argument('--len_kmer', action="store", dest='len_kmer', type=int, default=21, help="Length of kmers")
parser.add_argument('--p_value', action="store", dest='p_value', type=float, default=0.05, help="Threshold P-value to select kmers")
parser.add_argument('--remove_specific', action='store', dest='remove_specific', type=bool, default=False, help="Remove specific kmer from matrix")

args = parser.parse_args()

# --- 0. Print info of run in the log file
print("Matrix : ", args.matrix)
print("len_kmer : ", args.len_kmer)

def levenshtein_count(matrix, sep, len_kmer):
    # --- 1. First loop to get GC and TA values
    dico_count = {
        "c_count" : 0,
        "g_count" : 0,
        "t_count" : 0,
        "a_count" : 0,
        "count_all_bases": 0,
        "c_proportion": 0,
        "g_proportion": 0,
        "t_proportion": 0,
        "a_proportion": 0,
        "c_expected": 0,
        "g_expected": 0,
        "t_expected": 0,
        "a_expected": 0
    }
    with open(matrix, 'r') as file:
        for line in file:
            kmer_line = pd.read_csv(StringIO(line), sep=sep, index_col=0, header=None)
            kmer = str(kmer_line.iloc[0].name)
            dico_count["c_count"] += kmer.count("C")
            dico_count["g_count"] += kmer.count("G")
            dico_count["t_count"] += kmer.count("T")
            dico_count["a_count"] += kmer.count("A")
            dico_count["count_all_bases"] += 21

    #--- 2. Calculation of expected values for the selection
    dico_count["c_proportion"] = dico_count["c_count"] / dico_count["count_all_bases"]
    dico_count["g_proportion"] = dico_count["g_count"] / dico_count["count_all_bases"]
    dico_count["t_proportion"] = dico_count["t_count"] / dico_count["count_all_bases"]
    dico_count["a_proportion"] = dico_count["a_count"] / dico_count["count_all_bases"]
    dico_count["g_expected"] = dico_count["c_expected"] = (dico_count["g_proportion"] + dico_count["c_proportion"]) * len_kmer / 2
    dico_count["t_expected"] = dico_count["a_expected"] = (dico_count["t_proportion"] + dico_count["a_proportion"]) * len_kmer / 2
    print("G expected by kmer (calculated from kmer) :", dico_count["g_expected"])
    print("C expected by kmer (calculated from kmer) :", dico_count["c_expected"])
    print("T expected by kmer (calculated from kmer) :", dico_count["t_expected"])
    print("A expected by kmer (calculated from kmer) :", dico_count["a_expected"])
    return dico_count

