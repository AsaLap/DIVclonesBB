#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Antoine Laporte 2025

import bioutils

import argparse
import numpy as np
import os
import pandas as pd

parser = argparse.ArgumentParser(description='PCA on kmer matrices')
parser.add_argument('--matrix', action="store", dest='matrix', required=True, help="Path to matrix of kmer frequencies, TSV file, line names as first row")
parser.add_argument('--n_components', action="store", dest='n_components', default=10, help="Number of components to output")
parser.add_argument('--n_loadings', action="store", dest='n_loadings', default=50, help="Number of best loadings to get")
parser.add_argument('--draw_graphs', action="store", dest='draw_graphs', default=False, help="Do PCA graph or not + clustering with ward distance")

args = parser.parse_args()

# --- 0. Print info of run in the log file
print("Matrix : ", args.matrix)
print("Number of components : ", args.n_components)
print("Number of loadings : ", args.n_loadings)
print("Draw graphs : ", args.draw_graphs)


###------LOADING DATA------###
matrix = pd.read_csv(args.matrix, sep='\t', header=0, index_col=0)
n_components = int(args.n_components)
n_loadings = int(args.n_loadings)
###------END------###

###------PREPARING ENVIRONMENT------###
basename=os.path.basename(args.matrix)
print("Basename : ", basename)
main_dir = os.path.dirname(os.path.realpath(args.matrix))
print("Main directory : ", main_dir)
graph_dir = main_dir + "/PCA_graphs_" + basename.split(".")[0] #remove extension of basename
print("Graph directory : ", graph_dir)
###------END------###

###------COMPUTING PCA------###
df_pca, data_pca = bioutils.pca_computing(matrix, n_components=args.n_components)
###------END------###

#Plots
if args.draw_graphs:
    os.makedirs(graph_dir, exist_ok=True)
    ###------SPECIES SPECIFIC------###
    # Chenin
    groupes = matrix.columns.to_series().apply(bioutils.extraire_groupe_chenin)
    palette_groupes = {
        'AFS': "#435F55",
        'B': "#EE55AA",
        'BPacBio': "#EE5500"
    }
    ###------END------###

    df_pca["groupe"] = groupes

    ##Screeplot
    bioutils.pca_screeplot_seaborn(data_pca[1], save=graph_dir + "/PCA_" + basename, figsize=(15, 10))

    ##PC1-2
    bioutils.pca_scatterplot_seaborn(df_pca, data_pca, figsize=(15, 10), save=graph_dir + "/PCA_1_2_groups_" + basename, hue_legend="Groupe", hue="groupe", palette=palette_groupes, s=80)
    ##PC2-3
    bioutils.pca_scatterplot_seaborn(df_pca, data_pca, axes=("PC2", "PC3"), figsize=(15, 10), save=graph_dir + "/PCA_2_3_groups_" + basename, hue_legend="Groupe", hue="groupe", palette=palette_groupes, s=80)
    ##PC3-4
    bioutils.pca_scatterplot_seaborn(df_pca, data_pca, axes=("PC3", "PC4"), figsize=(15, 10), save=graph_dir + "/PCA_3_4_groups_" + basename, hue_legend="Groupe", hue="groupe", palette=palette_groupes, s=80)

###------GET LOADINGS VALUES------###
#Best Loadings, negative and positive
list_selected_pca_kmer = bioutils.pca_loadings_selection(data_pca[1], matrix.index)
print("Length of selected kmer : ", len(list_selected_pca_kmer))
#Selection of subset
matrix_pca_select = matrix.T[list_selected_pca_kmer].T
#Saving light matrix
matrix_pca_select.to_csv(main_dir + "/" + basename.split(".")[0] + "_" + str(n_loadings) + "_pca_loadings_" + str(n_components) + "_components.tsv", sep="\t")

###------CLUSTERING------###
if args.draw_graphs:
    bioutils.clustering(matrix_pca_select.T, save=graph_dir + "/cluster_euclid_ward_" + basename)