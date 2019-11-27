# Script to automate creation of input1 for samplesheet.txt file for use with vsearch script for fusion primers and paired-ends.
# 19.11.2019 LH
# Needs to be run in Python3

# Before using this script, the sample sheet from the lab must be made into the correct input.
# That is, 1st col is Sample_name, 2nd is Fusion_COI_i5_TAG_Primer, 3rd is Fusion_COI_i7_Primer.
# Everything else (other columns, and rows not in project) should be deleted from it.

# Give the name of the corrected sheet (as csv) as the arg value.
# e.g. python create_input1_file.py Fusion_COI_combi_MiSeq_Run2019_25.csv Sample_name Fusion_COI_i5_TAG_Primer Fusion_COI_i7_TAG_Primer

import argparse, sys

parser = argparse.ArgumentParser(description='Transform 3-column sample sheet into first input for samplesheet.txt.')
parser.add_argument('ModifiedSampleSheetCsv', help="Give the name of the modified sheet from lab (as csv, not tab-separated).")
parser.add_argument('Sample_name', help="Name of the first column (sample names)")
parser.add_argument('i5_TAG_Primer', help="Name of the second column (fwd primers)")
parser.add_argument('i7_TAG_Primer', help="Name of the third column (reverse primers)")

args = parser.parse_args()
#print(args.accumulate())


# Define a function for reverse-complementing.
def revcomp(seq):
    return seq.translate(str.maketrans('ACGTacgtRYMKrymkVBHDvbhd', 'TGCAtgcaYRKMyrkmBVDHbvdh'))[::-1]

# Read in mod sample sheet and create new file from it.
import csv

with open(sys.argv[1], 'r') as csvfile:
#    fieldnames = ['Sample_name', 'Fusion_COI_i5_TAG_Primer', 'Fusion_COI_i7_TAG_Primer']
    fieldnames = [sys.argv[2], sys.argv[3], sys.argv[4]]
    reader = csv.DictReader(csvfile, delimiter=',')
    for row in reader:
        r_rc = revcomp(row[sys.argv[4]])
        samplename = row[sys.argv[2]]
        corename = samplename.replace("_", "-")
        print(corename + "\t" + row[sys.argv[2]] + "\t" + row[sys.argv[3]] + "\t" + r_rc, file=open("input1.tsv","a"))

