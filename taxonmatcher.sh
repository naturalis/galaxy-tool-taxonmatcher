#!/bin/bash
#location for production server
#outlocation=$(mktemp -d /media/GalaxyData/database/files/XXXXXX)
#location for the testserver
#outlocation=$(mktemp -d /media/GalaxyData/files/XXXXXX)
outlocation=$(mktemp -d /home/galaxy/ExtraRef/XXXXXX)
if [ $3 == "nsr" ]
then
    taxonmatcher.py -i $1 -r $3 -t $2 -o $outlocation"/taxonmatched.txt" -n /home/galaxy/Tools/galaxy-tool-taxonmatcher/utilities/nsr_taxonmatcher
fi
mv $outlocation"/taxonmatched.txt" $4
rm -rf $outlocation