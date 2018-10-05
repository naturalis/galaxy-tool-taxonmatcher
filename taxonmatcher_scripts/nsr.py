#!/usr/bin/python3

from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import multiprocessing
from multiprocessing import Pool
from itertools import product
from functools import partial
import jellyfish
import sqlite3

class Nsr:
    def __init__(self, nsrReference):
        self.nsrDb = sqlite3.connect(nsrReference)
        self.nsrCursor = self.nsrDb.cursor()
        self.nsrReferenceSpeciesList = self.getSpeciesList()

    def match(self, names):
        pool = multiprocessing.Pool(processes=12)
        func = partial(self.fuzzy_match, self.nsrReferenceSpeciesList)
        results = []
        results = (pool.map_async(func, names))
        pool.close()
        pool.join()
        outputLines = []
        for name in results.get():
            fuzzy = ""
            if int(name[0]) < 3:
                fuzzyFlag = " fuzzy" if int(name[0]) != 0 else ""
                hit, matchType, synonymName = self.search_nsr(name[1], fuzzyFlag)
                outputLines.append([name[2], matchType, synonymName, hit[5],hit[11],hit[10],hit[9],hit[8],hit[7],hit[6], hit[-1]])
            else:
                outputLines.append([name[2], "not found in nsr", "", "", ""])
        return outputLines

    def fuzzy_match(self, nsrSpecies, x):
        best_match = process.extract(x.strip().lower(), nsrSpecies, limit=3)
        best_matchone = process.extractOne(x.strip(), nsrSpecies)
        dldistance = 9999
        bestHit = ""
        for match in best_match:
            a = jellyfish.damerau_levenshtein_distance(match[0].strip(), x.strip().lower())
            if a < dldistance:
                dldistance = a
                bestHit = (match[0].strip())
        return (str(dldistance), bestHit, x.strip())

    def search_nsr(self, name, fuzzyFlag):
        self.nsrCursor.execute("SELECT * FROM nsr WHERE species LIKE '%"+name.strip()+"%'")
        hit = self.nsrCursor.fetchone()
        if hit is not None:
            if hit[4] == "synonym":
                synonymName = hit[5]
                self.nsrCursor.execute("""SELECT * FROM nsr WHERE taxonID=?""", (str(hit[3]),))
                hit = self.nsrCursor.fetchone()
                return hit, "synonym"+fuzzyFlag, synonymName
            else:
                return hit, "match"+fuzzyFlag, ""
        else:
            return "", "Not found"


    def getSpeciesList(self):
        self.nsrCursor.execute("SELECT species FROM nsr")
        hits = self.nsrCursor.fetchall()
        allSpecies = []
        for x in hits:
            allSpecies.append(x[0])
        return allSpecies
