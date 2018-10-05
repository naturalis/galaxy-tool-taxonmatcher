#!/usr/bin/python3
from taxonmatcher_scripts.nsr import Nsr #Nederlands soorten register
import argparse
# Retrieve the commandline arguments
parser = argparse.ArgumentParser(description='taxonmatcher')
parser.add_argument('-i', '--input', metavar='namelist or blast output', dest='input', type=str, required=True)
parser.add_argument('-r', '--reference', metavar='taxonomy reference', dest='reference', type=str, required=True, choices=['nsr'])
parser.add_argument('-t', '--type', dest='type', type=str, required=True, choices=['nameslist', 'blast'])
parser.add_argument('-o', '--output', metavar='output', dest='output', type=str, required=True)
parser.add_argument('-n', '--nsr', help='nsr reference path', dest='nsr', type=str, required=False)
parser.add_argument('-g', '--gbif', help='gbif reference path', dest='gbif', type=str, required=False)
args = parser.parse_args()
if args.reference == "nrs":parser.error("missing -n/--nsr")

def get_input_list():
    namesList = []
    if args.type == "nameslist":
        with open(args.input, "r") as names:
            for x in names:
                namesList.append(x.strip())
    elif args.type == "blast":
        with open(args.input, "r") as blast:
            for x in blast:
                namesList.append(x.split("\t")[-1].split(" / ")[-1])
    return namesList

def main():
    names = get_input_list()
    if args.reference == "nsr":
        nsr = Nsr(args.nsr)
        matches = nsr.match(names)
        with open(args.output, "a") as output:
            output.write("\t".join(["#Input","#MatchType","#Synonym name","#Accepted name","#Kingdom","#Phylum","#Class","#Order","#Family","#Genus","#Metadata"]) + "\n")
            for x in matches:
                output.write("\t".join(x)+"\n")

if __name__ == "__main__":
    main()