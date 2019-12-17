# Script to automate creation of input1 and 2 for samplesheet.txt file for use with vsearch script for fusion primers and paired-ends.
# Last update: 16.12.2019 LH
# Needs to be run in Python3.

# Before using this script, the sample sheet from the lab must be made into the correct input.
# That is, 1st col is Sample_name, 2nd is Fusion_COI_i5_TAG_Primer, 3rd is Fusion_COI_i7_Primer.
# Everything else (other columns, and rows not in project) should be deleted from it.

# Give the name of the corrected sheet (as csv) as the arg value.
# e.g. python create_input1_file.py Fusion_COI_combi_MiSeq_Run2019_25.csv Sample_name Fusion_COI_i5_TAG_Primer Fusion_COI_i7_TAG_Primer

import argparse, sys

parser = argparse.ArgumentParser(description='Transform 3-column sample sheet into first input for samplesheet.txt.')
parser.add_argument('ModifiedSampleSheetCsv_name', nargs=1, help="Give the name of the modified sheet from lab (as csv, not tab-separated).")
parser.add_argument('Sample_name_colname', nargs='?', default="Sample_name", help="Name of the first column (sample names)")
parser.add_argument('i5_TAG_Primer_colname', nargs='?', default="Fusion_COI_i5_TAG_Primer", help="Name of the second column (fwd primers)")
parser.add_argument('i7_TAG_Primer_colname', nargs='?', default="Fusion_COI_i7_TAG_Primer", help="Name of the third column (reverse primers)")

args = parser.parse_args()


# Define a function for reverse-complementing.
def revcomp(seq):
    return seq.translate(str.maketrans('ACGTacgtRYMKrymkVBHDvbhd', 'TGCAtgcaYRKMyrkmBVDHbvdh'))[::-1]

# Check if output file already exists.
import os, warnings

if os.path.isfile('./input1.tsv'):
    warnings.warn('input1 file already exists! Appending to existing file. If you do not want this, delete input1.tsv and run this script again.')

# Read in mod sample sheet and create new file from it.
import csv

with open(sys.argv[1], 'r') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',')
    for row in reader:
        r_rc = revcomp(row[args.i7_TAG_Primer_colname])
        samplename = row[args.Sample_name_colname]
        corename = samplename.replace("_", "-")
        print(corename + "\t" + row[args.Sample_name_colname] + "\t" + row[args.i5_TAG_Primer_colname] + "\t" + r_rc, file=open("input1.tsv","a"))

# Check the generated file to see if underscores are in corenames (they shouldn't be).
with open('input1.tsv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    usc = 0
    for row in reader:
        corename = row[0]
        if "_" in corename:
            usc = usc + 1
            warnings.warn('Underscores in core fastq names! You may want to change these before proceeding further.')
    if usc == 0:
        print("")
        print("File input1_file.py successfully created.")
        print("")


# Create input2
if os.path.isfile('./input2.tsv'):
    warnings.warn('input2 file already exists! Appending to existing file. If you do not want this, delete input2.tsv and run this script again.')

f = os.popen("ls *_R1_001.fastq")
filenames = f.read()

for filename in filenames.split('\n'):
    print(filename.split('_')[0] + "\t" + filename, file=open("input2.tsv","a"))


print("File input2_file.py successfully created.")
print("")

f.close()
