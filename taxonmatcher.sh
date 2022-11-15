#!/bin/bash
outlocation=$(mktemp -d /data/files/XXXXXX)
SCRIPTDIR=$(dirname "$(readlink -f "$0")")

# sanity check
printf "Conda env: $CONDA_DEFAULT_ENV\n"
printf "Outlocation: $outlocation\n"
printf "Python version: $(python --version |  awk '{print $2}')\n"
printf "Biopython version: $(conda list | egrep biopython | awk '{print $2}')\n"
printf "Fuzzywuzzy version: $(conda list | egrep fuzzywuzzy | awk '{print $2}')\n"
printf "Jellyfish version: $(conda list | egrep jellyfish | awk '{print $2}')\n"
printf "Unzip version: $(unzip -v | head -n1 | awk '{print $2}')\n"
printf "Bash version: ${BASH_VERSION}\n"
printf "SCRIPTDIR: $SCRIPTDIR\n\n"

if [ $3 == "nsr" ]
then
    python3 $SCRIPTDIR"/taxonmatcherV2_multicore_gbif.py" -i $1 -r $3 -t $2 -o $outlocation"/taxonmatched.txt" -n /data/blast_databases/taxonomy/nsr_taxonmatcher
	echo "/data/blast_databases/taxonomy/nsr_taxonmatcher"
fi
if [ $3 == "gbif" ]
then
#    python3 $SCRIPTDIR"/taxonmatcherV2_multicore_gbif.py" -i $1 -r $3 -t $2 -o $outlocation"/taxonmatched.txt" -g /media/GalaxyData/blast_databases/taxonomy/gbif_taxonmatcher
#    echo "/media/GalaxyData/blast_databases/taxonomy/gbif_taxonmatcher"
    python3 $SCRIPTDIR"/taxonmatcherV2_multicore_gbif.py" -i $1 -r $3 -t $2 -o $outlocation"/taxonmatched.txt" -g /data/blast_databases/taxonomy/gbif_taxonmatcher
    echo "/data/blast_databases/taxonomy/gbif_taxonmatcher"
fi
mv $outlocation"/taxonmatched.txt" $4
rm -rf $outlocation
