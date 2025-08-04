#!/bin/sh
#SBATCH --job-name=levenshtein
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --mem=10000
#SBATCH --ntasks-per-node=1
#SBATCH --ntasks-per-core=1
#SBATCH --account=divclinesbb
#SBATCH --partition=divclonesbb

module purge
module load python/3.7.2

scripts_dir=$1
matrix=$2
names=$3
reads_count=$4
round=$5

python "$scripts_dir"/cluster_ponder_by_coverage.py \
--matrix "$matrix" \
--names "$names" \
--reads_count "$reads_count" \
--round "$round"
