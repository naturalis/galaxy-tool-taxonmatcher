#!/usr/bin/python3
import sqlite3
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
    with open("Taxa_tabular.txt", "r", encoding='latin-1') as nsr:#, encoding='latin-1'
        for line in nsr:
            line = line.strip().split("\t")
            species = line[2].replace(line[3].strip(), "")
            print(line)
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
    #cursor.execute("SELECT species FROM nsr WHERE species LIKE '%carex paniculata × remot%'")
    #print(cursor.fetchone()[0])
    cursor.execute("CREATE INDEX index_nsr_species ON nsr (species_rank);")
    #ursor.execute("CREATE INDEX index_gbif_genus ON gbif (genus);")

if __name__ == "__main__":
    main()
