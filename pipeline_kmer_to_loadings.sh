#!/bin/sh
# Antoine Laporte 2025
#SBATCH --job-name=KmerToLoadings
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --mem=10000
#SBATCH --ntasks-per-node=1
#SBATCH --ntasks-per-core=1
#SBATCH --account=divclinesbb
#SBATCH --partition=divclonesbb
#SBATCH -o slurm-%x.out

echo "Running on:$SLURM_NODELIST"
echo "Starting date: $(date +%d/%m/%y-%HH%M)"

#module purge
#module load python/3.7.2

# Loading parameters from config file
scripts_dir=$(pwd)
. "$scripts_dir"/run_parameters.config

printf "\Parameters:\n"
echo "matrix: $matrix"
echo "split_factor: $split_factor"
echo "reads_count: $reads_count"
echo "names: $names"
#echo "sep: $sep"
echo "round: $round"
echo "remove_specific: $remove_specific"
echo "a_percentage: $a_percentage"
echo "t_percentage: $t_percentage"
echo "c_percentage: $c_percentage"
echo "g_percentage: $g_percentage"
echo "len_kmer: $len_kmer"
echo "p_value: $p_value"

#Prepare filenames and output_directory
base_dir=$(dirname "$(realpath "$matrix")")
base_name=$(basename "${matrix}")
name=${base_name%%.*}
directory_output=${scripts_dir}/${name}_tmp

#making output directories
mkdir -p "${directory_output}"
mkdir -p "${base_dir}"/logs

printf "\n------SPLIT------\n"
#Counting number of lines to prepare the split
nb_lines=$(wc -l "$matrix" | awk '{ print $1 }')
lines=$((nb_lines / $split_factor + 1)) #+1 top avoid having a file with the rest of the euclidean division

echo "Original file contains $nb_lines lines"
echo "Splitting in $split_factor by files of $lines lines..."
START_TIME=$(date +%s)
split "$matrix" "${directory_output}/${name}" -l $lines -d --additional-suffix .tsv

ELAPSED=$(($(date +%s) - START_TIME))
echo "...splitting done!"
printf "Splitting time: %s\n\n" "$(date -d@$ELAPSED -u +%H\ hours\ %M\ min\ %S\ sec)"

printf "\n------PONDER------\n"
echo "Pondering each submatrix by coverage values..."
START_TIME=$(date +%s)
for file in "$directory_output"/*;
do
#  echo "$file"
  sbatch "$scripts_dir"/launch_ponder.sh \
  "$file" \
  "$names" \
  "$reads_count" \
  "$round";
done
ELAPSED=$(($(date +%s) - START_TIME))
echo "...pondering done!"
printf "Pondering time: %s\n\n" "$(date -d@$ELAPSED -u +%H\ hours\ %M\ min\ %S\ sec)"


printf "\n------LEVENSHTEIN------\n"
echo "Selecting kmer with Levenshtein process for each submatrix..."
START_TIME=$(date +%s)
for file in "$directory_output"/*pondered.tsv;
do
#  echo "$file";
  sbatch "$scripts_dir"/launch_levenshtein.sh \
  "$scripts_dir" \
  "$file" \
  "$remove_specific" \
  "$a_percentage" \
  "$t_percentage" \
  "$c_percentage" \
  "$g_percentage" \
  "$sep" \
  "$len_kmer" \
  "$p_value";
done
ELAPSED=$(($(date +%s) - START_TIME))
echo "...Levenshtein selection done!"
printf "Levenshtein time: %s\n\n" "$(date -d@$ELAPSED -u +%H\ hours\ %M\ min\ %S\ sec)"