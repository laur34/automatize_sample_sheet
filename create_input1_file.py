# Script to automate creation of input1 for samplesheet.txt file for use with vsearch script for fusion primers and paired-ends.
# 19.11.2019 LH
# Needs to be run in Python3

# Before using this script, the sample sheet from the lab must be made into the correct input.
# That is, 1st col is Sample_name, 2nd is Fusion_COI_i5_TAG_Primer, 3rd is Fusion_COI_i7_Primer.
# Everything else (other columns, and rows not in project) should be deleted from it.

# Give the name of the corrected sheet (as csv) as the arg value.
# e.g. python create_input1_file.py Fusion_COI_combi_MiSeq_Run2019_25.csv

import argparse, sys

parser = argparse.ArgumentParser()
parser.add_argument("ModifiedSampleSheetCsv", help="Give the name of the corrected sheet (as csv) as the arg value, e.g. python create_input1_file.py Fusion_COI_combi_MiSeq_Run2019_25.csv")
args = parser.parse_args()
#print(args.ModifiedSampleSheetCsv)


# Define a function for reverse-complementing.
def revcomp(seq):
    return seq.translate(str.maketrans('ACGTacgtRYMKrymkVBHDvbhd', 'TGCAtgcaYRKMyrkmBVDHbvdh'))[::-1]


import csv

with open(sys.argv[1], 'r') as csvfile:
    fieldnames = ['Sample_name', 'Fusion_COI_i5_TAG_Primer', 'Fusion_COI_i7_TAG_Primer']
    reader = csv.DictReader(csvfile, delimiter=',')
    for row in reader:
        r_rc = revcomp(row['Fusion_COI_i7_TAG_Primer'])
        samplename = row['Sample_name']
        corename = samplename.replace("_", "-")
        print(corename + "\t" + row['Sample_name'] + "\t" + row['Fusion_COI_i5_TAG_Primer'] + "\t" + r_rc, file=open("input1.tsv","a"))

