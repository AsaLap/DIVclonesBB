#!/bin/sh
#SBATCH --job-name=test
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --mem=100000
#SBATCH --ntasks-per-node=1
#SBATCH --ntasks-per-core=1
#SBATCH --partition=cpu
#SBATCH -o slurm-%x.out

echo "Running on:$SLURM_NODELIST"

module purge
module load python/3.7.2

python /storage/replicated/DIVclonesBB/02_scripts/ponder.py \
--matrix /storage/replicated/DIVclonesBB/04_kmer_matrices/PV_matrix.tsv \
--names /storage/replicated/DIVclonesBB/01_raw_data/club_des9/cepages/list_lines_petits_verdots_unique.txt \
--coverage /storage/replicated/DIVclonesBB/01_raw_data/club_des9/cepages/semillons_concatenated/reads_counts_petits_verdots_concatenated.txt

echo "Done"
