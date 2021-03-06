#!/usr/bin/python
"""
metapathways_last_to_megan.py

Created by Niels Hanson on 2013-08-16.
Copyright (c) 2013 Steven J. Hallam Laboratory. All rights reserved.
"""
from __future__ import division

__author__ = "Niels W Hanson"
__copyright__ = "Copyright 2013"
__credits__ = ["r"]
__version__ = "1.0"
__maintainer__ = "Niels W Hanson"
__status__ = "Release"

try:
     import os
     import re
     import sys
     import argparse
except:
     print """ Could not load some modules """
     print """ """
     sys.exit(3)


# Example: python metapathways_last_to_megan.py -i output/HOT_Sanger/*/blast_results/*cog*out.txt -o .
what_i_do = """Retrives read-taxonomy hits from the parsed (blast/last) result files <sample>.<database>.(blast/last)out.parsed.txt files, 
e.g. my_sample.refseq.lastout.parsed.txt, files from the <sample>/blast_results/ directory and formats them as .csv 
files for import into MEGAN. Requires that the database keep the taxonomy in within square braces, e.g. [E. coli K12].
"""
parser = argparse.ArgumentParser(description=what_i_do)
# add arguments to the parser
parser.add_argument('-i', dest='input_files', type=str, nargs='+',
                required=True, help='glob of <sample>.<database>.(blast/last)out.txt files from MetaPathways <sample>/blast_results/ output folder', default=None)                
parser.add_argument('-o', dest='output_dir', type=str, nargs='?',
                required=False, help='directory where <sample>.<database>.megan.csv.txt files will be put', default=os.getcwd())
parser.add_argument('--dsv', dest='dsv', action='store_true',
                required=False, help='flag to output a .dsv instread of a .csv file', default=False)
parser.add_argument('--count', dest='count', action='store_true',
                required=False, help='flag to output a count version of the file', default=False)
parser.add_argument('-d', dest='database', type=str, nargs='?', choices=['refseq', 'cog'],
                required=False, help='database parsing type: ether refseq style [E. coli] (default) or cog style', default="refseq")


def main(argv):
    args = vars(parser.parse_args())
    
    # setup input and output file_names
    input_files = args['input_files']
    output_dir = os.path.abspath(args['output_dir'])
    
    for f in input_files:
        file_handle = open(f, "r")
        lines = file_handle.readlines()
        file_handle.close()
        if args["database"] == "refseq":
            # refseq pattern
            brackets_pattern = re.compile(r"\[(.*?)\]")
        else:
            # cog pattern
            brackets_pattern = re.compile(r"# Organism: (.+) \(.+\)")
        
        end = ".csv.txt"
        if args['dsv']:
            end = ".dsv"
        sample_db = re.sub("\.(blast|last).*\.txt", "", os.path.basename(f), re.I)
        output_file = [output_dir, os.sep, sample_db, ".megan", end]
        output_handle = open("".join(output_file), "w")
        
        taxa_dictionary = {}
        if args['count']:
            for l in lines:
                fields = l.split("\t")
            	hits = brackets_pattern.findall(fields[9])
            	if hits:
            	   read = fields[0]
            	   last_score = fields[3]
            	   taxa = hits[-1]
            	   if taxa not in taxa_dictionary:
            	       taxa_dictionary[taxa] = 0
            	   taxa_dictionary[taxa] += 1
        else:
            for l in lines:
            	fields = l.split("\t")
            	hits = brackets_pattern.findall(fields[9])
            	if hits:
            	   read = fields[0]
            	   last_score = fields[3]
            	   taxa = hits[-1]
            	   out_line = read + ", " + taxa + ", " + last_score + "\n"
            	   output_handle.write(out_line)
        if args['count']:
            for t in taxa_dictionary:
                out_line = t + "," + str(taxa_dictionary[t]) + "\n"
                output_handle.write(out_line)
        output_handle.close()
    exit()

# the main function of metapaths
if __name__ == "__main__":
   main(sys.argv[1:])
