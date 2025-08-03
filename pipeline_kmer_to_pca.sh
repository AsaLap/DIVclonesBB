#!/bin/sh

# Antoine Laporte 2025


usage="Usage: mandatory: <kmer count tsv file> <split factor> <read count file> <names>\n
optional: <scripts_dir, default=/storage/replicated/DIVclonesBB/02_scripts>"

if [ -n "$1" ]; then
  echo "Matrix supplied: $1"
else
  echo "You need to supply the matrix as the first parameter!"
  echo "$usage"
  exit 1
fi
if [ -n "$2" ]; then
  echo "Split factor: $2"
else
  echo "You need to supply the split factor as the second parameter!"
  echo "$usage"
  exit 1
fi
if [ -n "$3" ]; then
  echo "Reads count supplied: $3"
else
  echo "You need to supply the reads count file as the third parameter!"
  echo "$usage"
  exit 1
fi
if [ -n "$4" ]; then
  echo "Names supplied: $4"
else
  echo "You need to supply the list of names as the fourth parameter!"
  echo "$usage"
  exit 1
fi

#echo "Running on:$SLURM_NODELIST"
#
#module purge
#module load python/3.7.2

echo "Starting date: $(date)"

matrix=$1
split_factor=$2
reads_count=$3
list_names=$4
scripts_dir=${5:-"/storage/replicated/DIVclonesBB/02_scripts"}
ARG6=${6:-$(date)}

echo "Optional arguments:"
echo "$scripts_dir"
echo "$ARG6"
#echo "$ARG3"
#echo "$ARG4"

#Prepare filenames and output_directory
base_dir=$(dirname "$(realpath "$matrix")")
base_name=$(basename "${matrix}")
name=${base_name%%.*}
directory_output=${base_dir}/${name}_tmp

#making output directory
mkdir -p "${directory_output}"

printf "\n------SPLIT------"
#Counting number of lines to prepare the split
nb_lines=$(wc -l "$matrix" | awk '{ print $1 }')
lines=$((nb_lines / $2 + 1)) #+1 top avoid having a file with the rest of the euclidean division

echo "Original file contains $nb_lines lines"
echo "Splitting in $split_factor by files of $lines lines"
#spliting file in wished number of files of equal size (except last one due to entire division)
START_TIME=$(date +%s)
split $matrix "${directory_output}/${name}" -l $lines -d --additional-suffix .tsv

ELAPSED=$(($(date +%s) - START_TIME))
printf "Splitting time: %s\n\n" "$(date -d@$ELAPSED -u +%H\ hours\ %M\ min\ %S\ sec)"
printf "------SPLIT------\n"

printf "\n------PONDER------"
for file in "$directory_output"/*;
do
  echo "$file"
  sbatch "$scripts_dir"/launch_ponder.sh \
  "$file" \
  "$names" \
  "$reads_count";
done
printf "------PONDER-END------\n"

printf "------LEVENSHTEIN------"
for file in "$directory_output"/*pondered.tsv;
do
  echo "$file"
  sbatch "$scripts_dir"/launch_levenshtein.sh \
  "$scripts_dir" \
  "$file"
  "$remove_specific" \
  "$p_value" \
  ;
done
