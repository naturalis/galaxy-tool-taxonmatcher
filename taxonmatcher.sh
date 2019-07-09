#!/bin/bash
outlocation=$(mktemp -d /media/GalaxyData/database/files/XXXXXX)
SCRIPTDIR=$(dirname "$(readlink -f "$0")")
if [ $3 == "nsr" ]
then
    python3 $SCRIPTDIR"/taxonmatcherV2_multicore_gbif.py" -i $1 -r $3 -t $2 -o $outlocation"/taxonmatched.txt" -n /media/GalaxyData/blast_databases/taxonomy/nsr_taxonmatcher
fi
if [ $3 == "gbif" ]
then
    python3 $SCRIPTDIR"/taxonmatcherV2_multicore_gbif.py" -i $1 -r $3 -t $2 -o $outlocation"/taxonmatched.txt" -g /media/GalaxyData/blast_databases/taxonomy/gbif_taxonmatcher
fi
mv $outlocation"/taxonmatched.txt" $4
rm -rf $outlocation
