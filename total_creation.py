# Script to automate creation samplesheet.txt file for use with vsearch script for fusion primers and paired-ends.
# Last update: 17.1.2020 LH
# Needs to be run in Python3.

# Before using this script, the sample sheet from the lab must be made into the correct input.
# That is, 1st col is Sample_name, 2nd is Fusion_COI_i5_TAG_Primer, 3rd is Fusion_COI_i7_TAG_Primer.
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
        try:
            r_rc = revcomp(row[args.i7_TAG_Primer_colname])
        except KeyError as err:
            print(err, "\n" + "Third column is not named Fusion_COI_i7_TAG_Primer. Please rename it, or specify current name as ARGV4.")
            sys.exit()
        try:
            samplename = row[args.Sample_name_colname]
            corename = samplename.replace("_", "-")
        except KeyError as err:
            print(err, "\n" + "First column is not named Sample_name. Please rename it, or specify current name as ARGV2.")
            sys.exit()
        try:
            print(corename + "\t" + row[args.Sample_name_colname] + "\t" + row[args.i5_TAG_Primer_colname] + "\t" + r_rc, file=open("input1.tsv","a"))
        except KeyError as err:
            print(err, "\n" + "Second column is not named Fusion_COI_i5_TAG_Primer. Please rename it, or specify current name as ARGV3.")
            sys.exit()


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
        print("File input1.tsv successfully created.")
        print("")


# Check if fastq files are in directory and there is the same number of them as sample sheet says.
import glob
fastqfiles = glob.glob("*_R1_001.fastq")

count = len(open('input1.tsv', 'r').readlines())
if count == len(fastqfiles):
    print("Fastq files found.")
    print("")
else:
    print("Number of forward fastq files in directory differs from number listed in input sample sheet!")
    print("Exiting")
    sys.exit()    


# Create input2
if os.path.isfile('./input2.tsv'):
    warnings.warn('input2 file already exists! Appending to existing file. If you do not want this, delete input2.tsv and run this script again.')


f2 = open('input2.tsv', 'w')
for fastqfile in fastqfiles:
    corename = fastqfile.split('_')[0]
    f2.write("{}\t".format(corename))
    f2.write("{}\n".format(fastqfile))

f2.close()

print("File input2.tsv successfully created.")
print("")


# Incorporating bash commands from joining.sh script.
# Using the shell way for now--this script is for local use only.
import subprocess
# Sorting
process = subprocess.run('sort -k1,1 input1.tsv > input1sorted.tsv', shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
process = subprocess.run('sort -k1,1 input2.tsv > input2sorted.tsv', shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Joining (original command is join -j1 input2sorted.tsv input1sorted.tsv -t $'\t' > joined.tsv)
process = subprocess.run('join -j1 input2sorted.tsv input1sorted.tsv > joined.tsv', shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Cutting the joined file to keep only wanted columns.
if os.path.isfile('./samplesheet.tsv'):
    warnings.warn('samplesheet.tsv file already exists! Appending to existing file. If you do not want this, delete samplesheet.tsv and run this script again.')

for line in open('joined.tsv'):
    col2 = line.rstrip('\n').split()[1]
    col4 = line.rstrip('\n').split()[3]
    col5 = line.rstrip('\n').split()[4]
    print(col2 + "\t" + col4 + "\t" + col5, file=open("samplesheet.tsv","a"))

# Replace raw fastq file endings with merged file endings.
with open('samplesheet.tsv', 'rt') as spltsv:
    with open('samplesheet.txt', 'wt') as spltxt:
        for line in spltsv:
            spltxt.write(line.replace('L001_R1_001.fastq','L001_merged.fq'))

print("File samplesheet.txt successfully created.")
print("")
print("Finished.")
#TODO: delete intermediate files.
