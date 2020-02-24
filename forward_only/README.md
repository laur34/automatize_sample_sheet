Automating creation of samplesheet.txt - Forward reads only!
============================================================

Especially in jobs with a lot of samples, you might want to run this script, instead of creating samplesheet.txt manually.

But it only works if you have fusion primers and paired-end reads.

This version is for when you can only use the forward reads, due to quality issues.

Copy the script (splsht_creation_Fwd_Only.py) into a directory where you want to run it, which must contain the following:
1. A **comma-separated** file based on the sample sheet from the lab, but with only 2 columns: "Sample_name" and "Fusion_COI_i5_TAG_Primer". Delete the rest (other columns, rows not in current project).
2. The raw forward .fastq files, which are named accordingly (they usually are already).

Minimal usage example: `python3 splsht_creation_Fwd_Only.py Ground_insects_samplesheet.csv`

Argv1 is the name of the two-column samplesheet. No other arguments are required if column names match the defaults (above).
Otherwise, you can specify the column names as Argv2 and 3, respectively, and then it will still work.

- Must use Python3.
- Tested on Python 3.7.3, Anaconda, Inc. on Linux, Ubuntu 18.04.3 LTS.

