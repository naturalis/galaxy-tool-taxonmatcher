# galaxy-tool-taxonmatcher
Find for your input taxonomy the taxonomy from an other database
## Getting Started
### Prerequisites
Jellyfish https://github.com/jamesturk/jellyfish<br />
fuzzy wuzzy https://github.com/seatgeek/fuzzywuzzy<br />
python3
### Installing
Installing the tool for use in Galaxy
```
cd /home/galaxy/Tools
```
```
sudo git clone https://github.com/naturalis/galaxy-tool-taxonmatcher
```
```
sudo chmod 777 galaxy-tool-taxonmatcher/taxonmatcher.py
```
```
sudo ln -s /home/galaxy/Tools/galaxy-tool-taxonmatcher/taxonmatcher.py /usr/local/bin/taxonmatcher.py
```
