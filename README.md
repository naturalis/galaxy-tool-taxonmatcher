# galaxy-tool-taxonmatcher
Find for your input taxonomy the taxonomy from an other database, currently GBIF (beta, memory consumption need to be improved) and The Dutch species register.
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
sudo git clone https://github.com/naturalis/galaxy-tool-taxonmatcher
```
### Creating the reference database for GBIF
Download the taxonomy backbone
```
wget http://rs.gbif.org/datasets/backbone/backbone-current.zip
```
unzip
```
unzip backbone-current.zip
```
Create the database (currently the path to Taxon.tsv is hardcoded)
```
python3 ../utilities/make_gbif_database.py
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
utilities/make_nsr_database.py
```
