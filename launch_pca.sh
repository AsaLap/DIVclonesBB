#!/bin/sh
# Antoine Laporte 2025
#SBATCH --job-name=pca
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --mem=100000
#SBATCH --ntasks-per-node=1
#SBATCH --ntasks-per-core=1
#SBATCH --account=divclinesbb
#SBATCH --partition=divclonesbb


module purge
module load python/3.7.2

scripts_dir=$1
matrix=$2

basename=$(basename "${matrix}")
#SBATCH -o logs/slurm-"$basename".out
echo "Running on:$SLURM_NODELIST"

python "$scripts_dir"/cluster_pca.py \
--matrix "$matrix"

echo "Done"
