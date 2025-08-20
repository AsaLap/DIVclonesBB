#!/bin/sh
# Antoine Laporte 2025
#SBATCH --job-name=pca
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --mem=10000
#SBATCH --ntasks-per-node=1
#SBATCH --ntasks-per-core=1
#SBATCH --partition=cpu
#SBATCH -o logs/pca."%j".out
#SBATCH -e logs/pca."%j".err

echo "Running on:$SLURM_NODELIST"

module purge
module load python/3.7.2

scripts_dir=$1
matrix=$2
n_components=$3
n_loadings=$4

echo "$matrix"

python "$scripts_dir"/cluster_pca.py \
--matrix "$matrix" \
--n_components "$n_components" \
--n_loadings "$n_loadings"

echo "Done"
