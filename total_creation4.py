# Script to automate creation samplesheet.txt file for use with vsearch script for fusion primers (and paired-ends.)
# Version 3.0 - 10.6.2021 - four columns of primers instead of two
# Needs to be run in Python3.

# Before using this script, the sample sheet from the lab must be made into the correct input.
# That is, 1st col is Sample_name, 2nd is Fusion_COI_i5_TAG_Primer, 3rd is Fusion_COI_i7_TAG_Primer.
# Everything else (other columns, and rows not in project) should be deleted from it.

# Give the name of the corrected sheet (as csv) as the arg value.
# e.g. python total_creation4.py splsht_MiSeq_Run2019_25.csv Sample_name Fusion_COI_i5_TAG_Primer Fusion_COI_i7_TAG_Primer

import argparse, sys

parser = argparse.ArgumentParser(description='Transform 3-column sample sheet into first input for samplesheet.txt.')
parser.add_argument('ModifiedSampleSheetCsv_name', nargs=1, help="Give the name of the modified sheet from lab (as csv, not tab-separated).")
parser.add_argument('Sample_name_colname', nargs='?', default="Sample_name", help="Name of the first column (sample names)")
parser.add_argument('i5_TAG_Primer_colname', nargs='?', default="Fusion_COI_i5_TAG_Primer", help="Name of the second column (fwd primers)")
parser.add_argument('i7_TAG_Primer_colname', nargs='?', default="Fusion_COI_i7_TAG_Primer", help="Name of the third column (reverse primers)")
parser.add_argument('merge_status', nargs='?', default="merged", help="merged or forward")

args = parser.parse_args()

import os, warnings, csv, glob

# Define a function for reverse-complementing.
def revcomp(seq):
    return seq.translate(str.maketrans('ACGTacgtRYMKrymkVBHDvbhd', 'TGCAtgcaYRKMyrkmBVDHbvdh'))[::-1]


# Implement check for intermediate files, with option to delete thm.
import subprocess
prev_run = os.path.isfile("samplesheet.txt") | os.path.isfile("input_1*.tsv") | os.path.isfile("input_2*.tsv") | os.path.isfile("joined.tsv") | os.path.isfile("samplesheet.tsv")

if prev_run:
    i = input('Intermediate files or output already exists. Delete them and continue (y/n)?\n')
    if i.lower() == 'yes' or i.lower() == 'y':
        if os.path.isfile("samplesheet.txt"):
            process = subprocess.Popen(['rm', 'samplesheet.txt'])
        if os.path.isfile("samplesheet.tsv"):
            process = subprocess.Popen(['rm', 'samplesheet.tsv'])
        if os.path.isfile("input1.tsv"):
            process = subprocess.Popen(['rm', 'input1.tsv'])
        if os.path.isfile("input2.tsv"):
            process = subprocess.Popen(['rm', 'input2.tsv'])
        if os.path.isfile("input1sorted.tsv"):
            process = subprocess.Popen(['rm', 'input1sorted.tsv'])
        if os.path.isfile("input2sorted.tsv"):
            process = subprocess.Popen(['rm', 'input2sorted.tsv'])   
    else:
        print("Please delete files from previous attempt, and try again.")
        sys.exit()
        


#TODO: remove below checks

# Define function to read in mod sample sheet and create new file (input1) from it, checking first if already exists in dir.
def createInput1file(splsht3col):
    with open(splsht3col, 'r') as csvfile:
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
                f_rc = revcomp(row[args.i5_TAG_Primer_colname])
            except KeyError as err:
                print("\n" + "Second column is not named Fusion_COI_i5_TAG_Primer. Please rename it, or specify current name as ARGV3")
                sys.exit()
            try:
                print(corename + "\t" + row[args.Sample_name_colname] + "\t" + row[args.i5_TAG_Primer_colname] + "\t" + r_rc + "\t" + row[args.i7_TAG_Primer_colname] + "\t" + f_rc, file=open("input1.tsv","a"))
            except KeyError as err:
                print(err, "\n" + "Second column is not named Fusion_COI_i5_TAG_Primer. Please rename it, or specify current name as ARGV3.")
                sys.exit()
    print("File input1.tsv successfully created.")



# Define fcn to check if underscores are present in any fastq file names in the directory:
def checkFASTQnamesForUsc():
    fwdfq = glob.glob("*_R1_001.fastq")
    for fastqname in fwdfq:
        parts = fastqname.split("_")
        if len(parts) > 5:
            print("Underscore in fastq file name detected!")
            print(parts)
            print("Exiting.")
            sys.exit()
    print("Forward FASTQ file names look ok.")
    print("")
    revfq = glob.glob("*_R2_001.fastq")
    for fastqname in revfq:
        parts = fastqname.split("_")
        if len(parts) > 5:
            print("Underscore in fastq file name detected!")
            print(parts)
            print("Exiting.")
            sys.exit()
    print("Reverse FASTQ file names look ok.")
    print("")



# Define fcn to check if fastq files are in directory and there is the same number of them as sample sheet says.
def CheckForFwdFastqs(sheet):
    fastqfiles = glob.glob("*_R1_001.fastq")
    count = len(open(sheet, 'r').readlines())
    if count == len(fastqfiles):
        print("Number of forward fastq files in directory matches number of lines to be written.")
        print("")
    else:
        print("Number of forward fastq files in directory differs from number listed on sample sheet!")
        print("Make sure all files are present, and names match (and no special characters in names).")
        print("Exiting")
        sys.exit()    


# Define fcn to create input2 file.
def createInput2file():
    fastqfiles = glob.glob("*_R1_001.fastq")
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

# Define a function to sort the two input files, and then join them into a new file.
def sortAndJoin():
    # Sorting
    process = subprocess.run('sort -k1,1 input1.tsv > input1sorted.tsv', shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process = subprocess.run('sort -k1,1 input2.tsv > input2sorted.tsv', shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Joining
    process = subprocess.run('join -j1 input2sorted.tsv input1sorted.tsv > joined.tsv', shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


# Define a function to cut the joined file, keeping only the wanted columns for samplesheet.
def cutColumns():
    for line in open('joined.tsv'):
        col2 = line.rstrip('\n').split()[1]
        col4 = line.rstrip('\n').split()[3]
        col5 = line.rstrip('\n').split()[4]
        col6 = line.rstrip('\n').split()[5]
        col7 = line.rstrip('\n').split()[6]
        print(col2 + "\t" + col4 + "\t" + col5 + "\t" + col6 + "\t" + col7, file=open("samplesheet.tsv","a"))


# Define a fcn to replace raw fastq file endings with merged file endings, and write the final output file.
def replaceEndingsAndWriteFinal():
    with open('samplesheet.tsv', 'rt') as spltsv:
        with open('samplesheet.txt', 'wt') as spltxt:
            for line in spltsv:
                if args.merge_status == 'merged':
                    spltxt.write(line.replace('L001_R1_001.fastq','L001_merged.fq'))
                else:
                    spltxt.write(line)
                    warnings.warn("Creating forward-only version of sheet.\n")
    print("File samplesheet.txt successfully created.")
    print("")


def removeIntFiles():
    print("Removing intermediate files.")
    print("")
    process = subprocess.Popen(['rm', 'input1.tsv'])
    process = subprocess.Popen(['rm', 'input2.tsv'])
    process = subprocess.Popen(['rm', 'input1sorted.tsv'])
    process = subprocess.Popen(['rm', 'input2sorted.tsv'])
    process = subprocess.Popen(['rm', 'joined.tsv'])
    process = subprocess.Popen(['rm', 'samplesheet.tsv'])



def main():
    checkFASTQnamesForUsc()
    createInput1file(sys.argv[1])
    createInput2file()
    sortAndJoin()
    cutColumns()
    CheckForFwdFastqs('samplesheet.tsv')
    replaceEndingsAndWriteFinal()
    removeIntFiles()
    print("Finished.")


if __name__ == '__main__':
    main()

