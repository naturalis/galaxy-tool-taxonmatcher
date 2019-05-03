#!/usr/bin/python3
import sqlite3
import csv

db = sqlite3.connect('gbif_taxonmatcher')
cursor = db.cursor()

def make_database():
    cursor.execute('''CREATE TABLE gbif(id INTEGER PRIMARY KEY, source TEXT, taxonID INTEGER, acceptedNameUsageID INTEGER, taxonomicStatus TEXT, species_rank TEXT, genus_rank TEXT, family_rank TEXT, order_rank TEXT, class_rank TEXT, phylum_rank TEXT, kingdom_rank TEXT, metadata TEXT)''')
    db.commit()

def add_nsr_taxonomy():
    with open("Taxon.tsv", "r", encoding='latin-1') as gbif, open("error_log.txt","a") as log:#, encoding='latin-1'
        for line in gbif:
            line = line.strip().split("\t")
            #print (line)
            try:
                if line[11] == "genus" or line[11] == "species" and line[17] != "incertae sedis":
                    try:
                        metadata = line[13].strip()
                    except:
                        metadata = ""
                    data = {"source":"gbif", "taxonID":line[0], "acceptedNameUsageID":line[3], "taxonomicStatus":line[14], "species_rank":line[7], "genus_rank":line[22].strip(), "family_rank":line[21], "order_rank":line[20],"class_rank":line[19], "phylum_rank":line[18], "kingdom_rank":line[17], "metadata":metadata}
                    cursor.execute('''INSERT INTO gbif(source, taxonID, acceptedNameUsageID, taxonomicStatus, species_rank, genus_rank, family_rank, order_rank, class_rank, phylum_rank, kingdom_rank, metadata)VALUES(:source, :taxonID, :acceptedNameUsageID, :taxonomicStatus, :species_rank, :genus_rank, :family_rank, :order_rank, :class_rank, :phylum_rank, :kingdom_rank, :metadata)''', data)
            except:
                log.write("\t".join(line)+"\n")
    db.commit()

def main():
    make_database()
    add_nsr_taxonomy()
    cursor.execute("CREATE INDEX index_gbif_species ON gbif (species_rank);")


if __name__ == "__main__":
    main()
