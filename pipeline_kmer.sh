#!/bin/sh

# Antoine Laporte 2025

#SBATCH --job-name=pipeline_kmer_petit_verdot
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --mem=120000
#SBATCH --ntasks-per-node=1
#SBATCH --ntasks-per-core=1
#SBATCH --account=divclinesbb
#SBATCH --partition=divclonesbb
#SBATCH -o slurm-%x.out

echo "Running on:$SLURM_NODELIST"
echo "%x"

module purge
module load python/3.7.2

#---Pondering---#
python /storage/replicated/DIVclonesBB/02_scripts/ponder_by_coverage.py \
--matrix /storage/replicated/DIVclonesBB/04_kmer_matrices/PV_matrix.tsv \
--coverage /storage/replicated/DIVclonesBB/01_raw_data/club_des9/cepages/petits_verdots_concatenated/reads_counts_petits_verdots_concatenated.txt \
--names /storage/replicated/DIVclonesBB/01_raw_data/club_des9/cepages/list_lines_petits_verdots_unique.txt \
#output=PV_matrix_pondered.tsv
echo "Pondering by coverage done..."

#---Levenshtein---#
python /storage/replicated/DIVclonesBB/02_scripts/levenshtein_on_cluster.py \
--matrix /storage/replicated/DIVclonesBB/04_kmer_matrices/PV_matrix_pondered.tsv \
--remove_specific=True
#output=PV_matrix_pondered_levenshtein.tsv
echo "Levenshtein selection done..."

#---PCA selection---#
python /storage/replicated/DIVclonesBB/02_scripts/pca_on_cluster.py \
--matrix /storage/replicated/DIVclonesBB/04_kmer_matrices/PV_matrix_pondered_levenshtein.tsv
#output=PV_matrix_pondered_levenshtein_xx_pca_loadings_xx_components.tsv
echo "Kmer loadings selection done..."