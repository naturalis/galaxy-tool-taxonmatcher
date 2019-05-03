#!/usr/bin/python3
import sqlite3
import csv
db = sqlite3.connect('nsr_taxonmatcher')
cursor = db.cursor()

def make_database():
    cursor.execute('''CREATE TABLE nsr(id INTEGER PRIMARY KEY, source TEXT, taxonID INTEGER, acceptedNameUsageID INTEGER, taxonomicStatus TEXT, species_rank TEXT, genus_rank TEXT, family_rank TEXT, order_rank TEXT, class_rank TEXT, phylum_rank TEXT, kingdom_rank TEXT, metadata TEXT)''')
    db.commit()


def check_unknowns(data):
    for x in data:
        if not data[str(x)]:
            data[str(x)] = "unknown "+str(x)
    return data

def add_nsr_taxonomy():
    with open("Taxa.txt", "r", encoding='latin-1') as csv_file:#, encoding='latin-1'
        nsr = csv.reader(csv_file, delimiter=',')
        for line in nsr:
            #line = line.strip().split("\t")
            species = line[2].replace(line[3].strip(), "")
            print(line)
            print(species)
            try:
                metadata = line[15]+";"+line[16]+";"+line[3]
            except:
                metadata = ""
            data = {"source":"nsr", "taxonID":line[0], "acceptedNameUsageID":line[1], "taxonomicStatus":line[4], "species_rank":species.strip(), "genus_rank":line[11].strip(), "family_rank":line[10], "order_rank":line[9],"class_rank":line[8], "phylum_rank":line[7], "kingdom_rank":line[6], "metadata":metadata}
            cursor.execute('''INSERT INTO nsr(source, taxonID, acceptedNameUsageID, taxonomicStatus, species_rank, genus_rank, family_rank, order_rank, class_rank, phylum_rank, kingdom_rank, metadata)VALUES(:source, :taxonID, :acceptedNameUsageID, :taxonomicStatus, :species_rank, :genus_rank, :family_rank, :order_rank, :class_rank, :phylum_rank, :kingdom_rank, :metadata)''', data)

    db.commit()


def main():
    make_database()
    add_nsr_taxonomy()
    cursor.execute("CREATE INDEX index_nsr_species ON nsr (species_rank);")

if __name__ == "__main__":
    main()
