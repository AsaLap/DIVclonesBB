#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Antoine Laporte 2025

import bioutils

import argparse
import pandas as pd

parser = argparse.ArgumentParser(description='PCA on kmer matrices')
parser.add_argument('--matrix', action="store", dest='matrix', required=True, help="Path to matrix of kmer frequencies, TSV file, line names as first row")
parser.add_argument('--n_components', action="store", dest='n_components', default=10, help="Number of components to output")
parser.add_argument('--n_loadings', action="store", dest='n_loadings', default=50, help="Number of best loadings to get")

args = parser.parse_args()

###------LOADING DATA------###
matrix = pd.read_csv(args.matrix, sep='\t', header=0, index_col=0)
n_components = int(args.n_components)
n_loadings = int(args.n_loadings)
###------END------###

###------COMPUTING PCA------###
df_pca, data_pca = bioutils.pca_computing(matrix, n_components=args.n_components)
###------END------###

###------GET LOADINGS VALUES------###
#Best Loadings, negative and positive
list_selected_pca_kmer = bioutils.pca_loadings_selection(data_pca[1], matrix.index)
print("Length of selected kmer : ", len(list_selected_pca_kmer))
#Selection of subset
matrix_pca_select = matrix.T[list_selected_pca_kmer].T
#Saving light matrix
matrix_pca_select.to_csv(args.matrix.split(".")[0] + "_" + str(n_loadings) + "_pca_loadings_" + str(n_components) + "_components.tsv", sep="\t")