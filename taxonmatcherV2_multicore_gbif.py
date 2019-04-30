#!/usr/bin/python3
#from taxonmatcher_scripts.nsr_list import Nsrlist #Nederlands soorten register
import argparse
import sqlite3
import multiprocessing
from multiprocessing import Pool
from functools import partial
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import jellyfish
# Retrieve the commandline arguments
parser = argparse.ArgumentParser(description='taxonmatcher')
parser.add_argument('-i', '--input', metavar='namelist or blast output', dest='input', type=str, required=True)
parser.add_argument('-r', '--reference', metavar='taxonomy reference', dest='reference', type=str, required=True, choices=['nsr', 'gbif'])
parser.add_argument('-t', '--type', dest='type', type=str, required=True, choices=['nameslist', 'blast'])
parser.add_argument('-o', '--output', metavar='output', dest='output', type=str, required=True)
parser.add_argument('-n', '--nsr', help='nsr reference path', dest='nsr', type=str, required=False)
parser.add_argument('-g', '--gbif', help='gbif reference path', dest='gbif', type=str, required=False)
args = parser.parse_args()
if args.reference == "nsr" and args.nsr is None:
    parser.error("missing -n/--nsr nsr sqlite reference")
if args.reference == "gbif" and args.gbif is None:
    parser.error("missing -g/--gbif gbif sqlite reference")

def write_header():
    if args.reference == "nsr" or args.reference == "gbif":
        with open(args.output, "a") as output:
            output.write("\t".join(["#Input","#MatchType","#Synonym","#Accepted name","#Taxon rank", "#Kingdom","#Phylum","#Class","#Order","#Family","#Genus","#Metadata","#Input read"]) + "\n")

def read_blast_input():
    taxonomyHits = []
    with open(args.input,"r") as input:
        for line in input:
            if line.split("\t")[0] != "#Query ID":
                line = line.strip()
                hit = []
                hit.append(line.split("\t")[0])
                hit.append(line.split("\t")[-1].split(" / "))
                taxonomyHits.append(hit)
    return taxonomyHits

def read_nameslist_input():
    taxonomyHits = []
    with open(args.input,"r") as input:
        for line in input:
            if line[0] != "#":
                taxonomyHits.append(line.strip())
    return taxonomyHits

def getSpeciesList(nsrCursor):
    if args.reference == "nsr":
        nsrDb = sqlite3.connect(args.nsr)
        nsrCursor = nsrDb.cursor()
        table = "nsr"
    if args.reference == "gbif":
        nsrDb = sqlite3.connect(args.gbif)
        nsrCursor = nsrDb.cursor()
        table = "gbif"
    nsrCursor.execute("SELECT species_rank FROM "+table)
    hits = nsrCursor.fetchall()
    allSpecies = []
    for x in hits:
        allSpecies.append(x[0].lower())
    return allSpecies

def getGenusList(nsrCursor):
    if args.reference == "nsr":
        nsrDb = sqlite3.connect(args.nsr)
        nsrCursor = nsrDb.cursor()
        table = "nsr"
    if args.reference == "gbif":
        nsrDb = sqlite3.connect(args.gbif)
        nsrCursor = nsrDb.cursor()
        table = "gbif"

    nsrCursor.execute("SELECT genus_rank FROM "+table)
    hits = nsrCursor.fetchall()
    allGenera = []
    for x in hits:
        allGenera.append(x[0].lower())
    return allGenera

def matchSpeciesGenus(taxonomyList, taxonomyHit, rank):
    #score, input, match, taxon of match, matchtype
    if taxonomyHit.lower() in taxonomyList:
        return [0, taxonomyHit, taxonomyHit, rank, "match"]
    else:
        best_match = process.extract(taxonomyHit.lower(), taxonomyList, limit=3)
        dldistance = 9999
        bestHit = ""
        for match in best_match:
            a = jellyfish.damerau_levenshtein_distance(match[0].strip(), taxonomyHit.lower())
            if a < dldistance:
                dldistance = a
                bestHit = (match[0].strip())
        if int(dldistance) < 3:
            return [str(dldistance), taxonomyHit, bestHit, rank, "fuzzy"]
        else:
            return False

def matchFamily(taxonomyHit, rank):
    if args.reference == "nsr":
        nsrDb = sqlite3.connect(args.nsr)
        nsrCursor = nsrDb.cursor()
        table = "nsr"
    if args.reference == "gbif":
        nsrDb = sqlite3.connect(args.gbif)
        nsrCursor = nsrDb.cursor()
        table = "gbif"

    nsrCursor.execute("SELECT * FROM {table} WHERE {column} = '{name}' COLLATE NOCASE".format(table=table, column=rank, name=taxonomyHit))
    hit = nsrCursor.fetchone()
    rankNumbers = {"family_rank":7, "order_rank":8, "class_rank":9, "phylum_rank":10, "kingdom_rank":11}
    if hit is not None:
        return [0, taxonomyHit, hit[rankNumbers[rank]], rank, "match"]
    else:
        nsrCursor.execute("SELECT DISTINCT {column} FROM {table}".format(column=rank, table=table))
        hit = nsrCursor.fetchall()
        familyList = []
        if hit is not None:
            for x in hit:
                familyList.append(x[0].lower())
        best_match = process.extract(taxonomyHit.lower(), familyList, limit=3)
        dldistance = 9999
        bestHit = ""
        for match in best_match:
            a = jellyfish.damerau_levenshtein_distance(match[0].strip(), taxonomyHit.lower())
            if a < dldistance:
                dldistance = a
                bestHit = (match[0].strip())
        if int(dldistance) < 3:
            return [str(dldistance), taxonomyHit, bestHit, rank, "fuzzy"]
        else:
            return False

def matchExact(speciesList, genusList, taxonomyHit):
    if args.reference == "nsr":
        nsrDb = sqlite3.connect(args.nsr)
        nsrCursor = nsrDb.cursor()
        table = "nsr"
    if args.reference == "gbif":
        nsrDb = sqlite3.connect(args.gbif)
        nsrCursor = nsrDb.cursor()
        table = "gbif"

    if taxonomyHit.lower() in speciesList:
        return [0, taxonomyHit, taxonomyHit, "species_rank", "match"]
    elif taxonomyHit.lower() in genusList:
        return [0, taxonomyHit, taxonomyHit, "genus_rank", "match"]
    else:
        rankNumbers = {"family_rank":7, "order_rank":8, "class_rank":9, "phylum_rank":10, "kingdom_rank":11}
        rankList = {"family_rank", "order_rank", "class_rank", "phylum_rank"}
        for rank in rankList:
            nsrCursor.execute("SELECT * FROM {table} WHERE {column} = '{name}' COLLATE NOCASE".format(table=table, column=rank, name=taxonomyHit))
            hit = nsrCursor.fetchone()
            if hit is not None:
                return [0, taxonomyHit, hit[rankNumbers[rank]], rank, "match"]
            else:
                pass
        return False

def get_entry_from_database(match):
    if args.reference == "nsr":
        nsrDb = sqlite3.connect(args.nsr)
        nsrCursor = nsrDb.cursor()
        table = "nsr"
    if args.reference == "gbif":
        nsrDb = sqlite3.connect(args.gbif)
        nsrCursor = nsrDb.cursor()
        table = "gbif"

    nsrCursor.execute("SELECT * FROM {table} WHERE {column} = '{name}' COLLATE NOCASE".format(table=table, column=match[-2], name=match[-3]))
    hit = nsrCursor.fetchone()
    if hit is not None:
        if hit[4] == "synonym":
            synonymName = hit[5]
            params = (str(hit[3]),)
            nsrCursor.execute("SELECT * FROM {table} WHERE taxonID=?".format(table=table), params)
            hit = nsrCursor.fetchone()
            #output = outputLines.append([name[2], matchType, synonymName, hit[5],hit[11],hit[10],hit[9],hit[8],hit[7],hit[6], hit[-1]]
            return [hit, "synonym"]
        else:
            return [hit, "match"]
    else:
        #extra check
        return False

def create_output_line_blast(databaseHit, match, input):
    if databaseHit:
        if match[3] == "species_rank":
            output = [" / ".join(input[1]), match[-1], databaseHit[1],databaseHit[0][5],match[3][0:-5], databaseHit[0][11],databaseHit[0][10],databaseHit[0][9],databaseHit[0][8],databaseHit[0][7],databaseHit[0][6], databaseHit[0][-1],input[0]]
        elif match[3] == "genus_rank":
            output = [" / ".join(input[1]), match[-1], databaseHit[1],databaseHit[0][6],match[3][0:-5], databaseHit[0][11],databaseHit[0][10],databaseHit[0][9],databaseHit[0][8],databaseHit[0][7],databaseHit[0][6], "", input[0]]
        elif match[3] == "family_rank":
            output = [" / ".join(input[1]), match[-1], databaseHit[1],databaseHit[0][7],match[3][0:-5], databaseHit[0][11],databaseHit[0][10],databaseHit[0][9],databaseHit[0][8],databaseHit[0][7], "", "",input[0]]
        elif match[3] == "order_rank":
            output = [" / ".join(input[1]), match[-1], databaseHit[1],databaseHit[0][8],match[3][0:-5], databaseHit[0][11],databaseHit[0][10],databaseHit[0][9],databaseHit[0][8],"", "", "",input[0]]
        elif match[3] == "class_rank":
            output = [" / ".join(input[1]), match[-1], databaseHit[1],databaseHit[0][9],match[3][0:-5], databaseHit[0][11],databaseHit[0][10],databaseHit[0][9],"","", "", "",input[0]]
        elif match[3] == "phylum_rank":
            output = [" / ".join(input[1]), match[-1], databaseHit[1],databaseHit[0][10],match[3][0:-5], databaseHit[0][11],databaseHit[0][10],"","","", "", "",input[0]]

    else:
        output = [" / ".join(input[1]), "Not found", "","","", "","","","","", "", "",input[0]]
    return output

def create_output_line_nameslist(databaseHit, match, input):
    if databaseHit:
        if match[3] == "species_rank":
            output = [input, match[-1], databaseHit[1],databaseHit[0][5],match[3][0:-5], databaseHit[0][11],databaseHit[0][10],databaseHit[0][9],databaseHit[0][8],databaseHit[0][7],databaseHit[0][6], databaseHit[0][-1], ""]
        elif match[3] == "genus_rank":
            output = [input, match[-1], databaseHit[1],databaseHit[0][6],match[3][0:-5], databaseHit[0][11],databaseHit[0][10],databaseHit[0][9],databaseHit[0][8],databaseHit[0][7],databaseHit[0][6], "", ""]
        elif match[3] == "family_rank":
            output = [input, match[-1], databaseHit[1],databaseHit[0][7],match[3][0:-5], databaseHit[0][11],databaseHit[0][10],databaseHit[0][9],databaseHit[0][8],databaseHit[0][7], "", "",""]
        elif match[3] == "order_rank":
            output = [input, match[-1], databaseHit[1],databaseHit[0][8],match[3][0:-5], databaseHit[0][11],databaseHit[0][10],databaseHit[0][9],databaseHit[0][8],"", "", "",""]
        elif match[3] == "class_rank":
            output = [input, match[-1], databaseHit[1],databaseHit[0][9],match[3][0:-5], databaseHit[0][11],databaseHit[0][10],databaseHit[0][9],"","", "", "",""]
        elif match[3] == "phylum_rank":
            output = [input, match[-1], databaseHit[1],databaseHit[0][10],match[3][0:-5], databaseHit[0][11],databaseHit[0][10],"","","", "", "",""]

    else:
        output = [input, "Not found", "","","", "","","","","", "", "", ""]
    return output

def match_blast(speciesList, genusList, taxonomyHit):
    match = False
    if "unknown" not in taxonomyHit[1][-1].lower():
        match = matchSpeciesGenus(speciesList, taxonomyHit[1][-1], "species_rank")
    if "unknown" not in taxonomyHit[1][-2].lower() and not match:
        match = matchSpeciesGenus(genusList, taxonomyHit[1][-2], "genus_rank")
    #add functions for higher ranks here
    if "unknown" not in taxonomyHit[1][-3].lower() and not match:
        match = matchFamily(taxonomyHit[1][-3], "family_rank")
    if "unknown" not in taxonomyHit[1][-4].lower() and not match:
        match = matchFamily(taxonomyHit[1][-4], "order_rank")
    if "unknown" not in taxonomyHit[1][-5].lower() and not match:
        match = matchFamily(taxonomyHit[1][-5], "class_rank")
    if "unknown" not in taxonomyHit[1][-6].lower() and not match:
        match = matchFamily(taxonomyHit[1][-6], "phylum_rank")

    outputLine = []
    if match:
        databaseHit = get_entry_from_database(match)
    else:
        databaseHit = False
    output = create_output_line_blast(databaseHit, match, taxonomyHit)
    return output

def match_nameslist(speciesList, genusList, taxonomyHit):
    match = False
    #Check exact matches first
    if "unknown" not in taxonomyHit.lower():
        match = matchExact(speciesList, genusList, taxonomyHit)
    if "unknown" not in taxonomyHit.lower() and not match:
        match = matchSpeciesGenus(speciesList, taxonomyHit, "species_rank")
    if "unknown" not in taxonomyHit.lower() and not match:
        match = matchSpeciesGenus(genusList, taxonomyHit, "genus_rank")
    #add functions for higher ranks here
    if "unknown" not in taxonomyHit.lower() and not match:
        match = matchFamily(taxonomyHit, "family_rank")
    if "unknown" not in taxonomyHit.lower() and not match:
        match = matchFamily(taxonomyHit, "order_rank")
    if "unknown" not in taxonomyHit.lower() and not match:
        match = matchFamily(taxonomyHit, "class_rank")
    if "unknown" not in taxonomyHit.lower() and not match:
        match = matchFamily(taxonomyHit, "phylum_rank")

    outputLine = []
    if match:
        databaseHit = get_entry_from_database(match)
    else:
        databaseHit = False
    output = create_output_line_nameslist(databaseHit, match, taxonomyHit)
    return output

def taxonmatch_nsr_blast():
    if args.reference == "nsr":
        nsrDb = sqlite3.connect(args.nsr)
        nsrCursor = nsrDb.cursor()
    if args.reference == "gbif":
        nsrDb = sqlite3.connect(args.gbif)
        nsrCursor = nsrDb.cursor()
    taxonomyHits = read_blast_input()
    speciesList = getSpeciesList(nsrCursor)
    genusList = getGenusList(nsrCursor)
    pool = multiprocessing.Pool(processes=12)
    func = partial(match_blast, speciesList, genusList)
    results = []
    results = (pool.map_async(func, taxonomyHits))
    pool.close()
    pool.join()
    with open(args.output, "a") as outputFile:
        for result in results.get():
            outputFile.write("\t".join(result)+"\n")

def taxonmatch_nsr_nameslist():
    if args.reference == "nsr":
        nsrDb = sqlite3.connect(args.nsr)
        nsrCursor = nsrDb.cursor()
    if args.reference == "gbif":
        nsrDb = sqlite3.connect(args.gbif)
        nsrCursor = nsrDb.cursor()


    taxonomyHits = read_nameslist_input()
    speciesList = getSpeciesList(nsrCursor)
    genusList = getGenusList(nsrCursor)
    pool = multiprocessing.Pool(processes=12)
    func = partial(match_nameslist, speciesList, genusList)
    results = []
    results = (pool.map_async(func, taxonomyHits))
    pool.close()
    pool.join()
    with open(args.output, "a") as outputFile:
        for result in results.get():
            outputFile.write("\t".join(result)+"\n")

def main():
    write_header()
    if args.type == "nameslist":
        taxonmatch_nsr_nameslist()
    elif args.type == "blast":
        taxonmatch_nsr_blast()

def test_database():
    nsrCursor = sqlite3.connect(args.nsr).cursor()
    nsrCursor.execute("SELECT * FROM nsr WHERE {column} = '{name}'".format(column="genus", name="Cryptotendipes"))
    hit = nsrCursor.fetchone()
    if hit is not None:
        print(hit)

if __name__ == "__main__":
    main()
    #test_database()
