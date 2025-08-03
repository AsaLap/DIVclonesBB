#!/bin/sh
#SBATCH --job-name=levenshtein
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --mem=10000
#SBATCH --ntasks-per-node=1
#SBATCH --ntasks-per-core=1
#SBATCH --account=divclinesbb
#SBATCH --partition=divclonesbb
#SBATCH -o slurm-%x.out

echo "Running on:$SLURM_NODELIST"

module purge
module load python/3.7.2

scripts_dir=$1
matrix=$2

python "$scripts_dir"/levenshtein_on_cluster.py \
--matrix "$matrix" \

echo "Done"
