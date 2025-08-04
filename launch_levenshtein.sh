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
remove_specific=$3
a_percentage=$4
t_percentage=$5
c_percentage=$6
g_percentage=$7
sep=$8
len_kmer=$9
p_value=${10}

basename=$(basename "${matrix}")
#SBATCH -o logs/slurm-"$basename".out
echo "Running on:$SLURM_NODELIST"

python "$scripts_dir"/cluster_levenshtein.py \
--matrix "$matrix" \
--remove_specific "$remove_specific" \
--a_percentage "$a_percentage" \
--t_percentage "$t_percentage" \
--c_percentage "$c_percentage" \
--g_percentage "$g_percentage" \
--sep "$sep" \
--len_kmer "$len_kmer" \
--p_value "$p_value"
