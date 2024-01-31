# galaxy-tool-taxonmatcher
Find for your input taxonomy the taxonomy from an other database, currently GBIF and The Dutch species register.  

## Installation
### Manual
Clone this repo in your Galaxy ***Tools*** directory:  
`git clone https://github.com/naturalis/galaxy-tool-taxonmatcher`  

Make the python script executable:  
`chmod 755 galaxy-tool-taxonmatcher/taxonmatcher.sh`  
`chmod 755 galaxy-tool-taxonmatcher/taxonmatcher.py` 

Append the file ***tool_conf.xml***:    
`<tool file="/path/to/Tools/galaxy-tool-taxonmatcher/taxonmatcher.sh" />`  

### Ansible
Depending on your setup the [ansible.builtin.git](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/git_module.html) module could be used.  
[Install the tool](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/git_module.html#examples) 
by including the following in your dedicated ***.yml** file:  

`  - repo: https://github.com/naturalis/galaxy-tool-taxonmatcher`  
&ensp;&ensp;`file: taxonmatcher.xml`  
&ensp;&ensp;`version: master`  

### Note
The instructions above assume python3 and gcc compiler are installed.  

## Create reference databases  
The steps below shoud be executed from the galaxy-tool-taxonmatcher folder  
in your Galaxy ***Tools*** directory.  

### Creating the reference database for GBIF
Download the taxonomy backbone  
`wget https://hosted-datasets.gbif.org/datasets/backbone/current/backbone.zip`  
unzip  
`unzip -p backbone.zip Taxon.tsv > Taxon.tsv`  
Taxon.tsv should be in path/to/galaxy-tool-taxonmatcher/  
Create the database (currently the path to Taxon.tsv is hardcoded)  
`python3 utilities/make_gbif_database.py`  
The output file is **gbif_taxonmatcher**  

### Creating the reference database for The Dutch species register  
Download the taxonomy backbone  
`wget http://api.biodiversitydata.nl/v2/taxon/dwca/getDataSet/nsr`  
unzip  
`unzip -p nsr Taxa.txt > Taxa.txt`  
Taxa.txt should be in path/to/galaxy-tool-taxonmatcher/  
Create the database (currently the path to Taxon.txt is hardcoded)  
`python3 utilities/make_nsr_database.py`  
The output file is **nsr_taxonmatcher**  

### Specify database file location  
Move the database files (gbif_taxonmatcher and nsr_taxonmatcher) to the desired location  
(in our case: /data/blast_databases/taxonomy/). Make sure the path in **taxonmatcher.sh**  
corresponds to this location.  
