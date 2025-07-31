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

python /storage/replicated/DIVclonesBB/02_scripts/levenshtein_count.py \
--matrix /storage/replicated/DIVclonesBB/04_kmer_matrices/PV_matrix.tsv \

echo "Done"
