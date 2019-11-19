# Script to automate creation of input1 for samplesheet.txt file for use with vsearch script for fusion primers and paired-ends.
# 18.11.2019 LH
# Needs to be run in Python3

# Before using this script, the sample sheet from the lab must be made into the correct input.
# That is, 1st col is Sample_name, 2nd is Fusion_COI_i5_TAG_Primer, 3rd is Fusion_COI_i7_Primer.
# Everything else (other columns, and rows not in project) should be deleted from it.


# Define a function for reverse-complementing.
def revcomp(seq):
    return seq.translate(str.maketrans('ACGTacgtRYMKrymkVBHDvbhd', 'TGCAtgcaYRKMyrkmBVDHbvdh'))[::-1]



import csv

with open('Fusion_COI_combi_MiSeq_Run2019_25.csv') as csvfile:
    fieldnames = ['Sample_name', 'Fusion_COI_i5_TAG_Primer', 'Fusion_COI_i7_TAG_Primer']
    reader = csv.DictReader(csvfile, delimiter=',')
    for row in reader:
        r_rc = revcomp(row['Fusion_COI_i7_TAG_Primer'])
        samplename = row['Sample_name']
        corename = samplename.replace("_", "-")
#        spl_sheet_line = ''
#        spl_sheet_line += corename + "\t" + row['Sample_name'] + "\t" + row['Fusion_COI_i5_TAG_Primer'] + "\t" + r_rc
#        print(spl_sheet_line)
        print(corename + "\t" + row['Sample_name'] + "\t" + row['Fusion_COI_i5_TAG_Primer'] + "\t" + r_rc, file=open("input1.tsv","a"))

