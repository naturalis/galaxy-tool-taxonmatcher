#!/bin/bash
outlocation=$(mktemp -d /home/galaxy/galaxy/database/XXXXXX)
SCRIPTDIR=$(dirname "$(readlink -f "$0")")
which python3
if [ $3 == "nsr" ]
then
    python3 $SCRIPTDIR"/taxonmatcherV2_multicore_gbif.py" -i $1 -r $3 -t $2 -o $outlocation"/taxonmatched.txt" -n /home/galaxy/Tools/galaxy-tool-taxonmatcher/nsr_taxonmatcher
fi
if [ $3 == "gbif" ]
then
    python3 $SCRIPTDIR"/taxonmatcherV2_multicore_gbif.py" -i $1 -r $3 -t $2 -o $outlocation"/taxonmatched.txt" -g /home/galaxy/Tools/galaxy-tool-taxonmatcher/test/gbif_taxonmatcher2
fi
mv $outlocation"/taxonmatched.txt" $4
rm -rf $outlocation
