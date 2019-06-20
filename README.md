# galaxy-tool-taxonmatcher
Find for your input taxonomy the taxonomy from an other database, currently GBIF (beta, memory consumption need to be improved) and The Dutch species register.

NOTE:
This script is now back in a somewhat beta fase due to the addition of gbif and later added functionalities. The code should be re-written in a more logic and efficient way. The script works but is not heavely tested. 

## Getting Started
### Prerequisites
Jellyfish https://github.com/jamesturk/jellyfish<br />
```
pip install jellyfish
```
fuzzy wuzzy https://github.com/seatgeek/fuzzywuzzy<br />
```
pip install fuzzywuzzy[speedup]
```
NOTE: **fuzzywuzzy** requires `gcc` to be installed. If this is not the case,
run ```sudo apt install gcc ``` (user: ***ubuntu***) first. 

biopython
```
pip install biopython
```
python3
### Installing
Installing the tool for use in Galaxy
```
cd /home/galaxy/Tools
```
```
git clone https://github.com/naturalis/galaxy-tool-taxonmatcher
```
### Creating the reference database for GBIF
Download the taxonomy backbone
```
cd /home/galaxy/Tools/galaxy-tool-taxonmatcher
```
```
wget http://rs.gbif.org/datasets/backbone/backbone-current.zip
```
unzip
```
unzip -p backbone-current.zip Taxon.tsv > Taxon.tsv
```
Create the database (currently the path to Taxon.tsv is hardcoded)
```
python3 utilities/make_gbif_database.py
```
### Creating the reference database for The Dutch species register
Download the taxonomy backbone
```
wget http://api.biodiversitydata.nl/v2/taxon/dwca/getDataSet/nsr
```
unzip
```
unzip nsr
```
Create the database (currently the path to Taxon.txt is hardcoded)
```
python 3 utilities/make_nsr_database.py
```
Add the path to the database files (nsr_taxonmatcher and gbif_taxonmatcher) to taxonmatcher.sh
<br />
Add the following line to /home/galaxy/galaxy/config/tool_conf.xml
```
<tool file="/home/galaxy/Tools/galaxy-tool-taxonmatcher/taxonmatcher.xml" />
```
