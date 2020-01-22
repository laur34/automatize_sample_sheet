Automating creation of samplesheet.txt
======================================

Especially in jobs with a lot of samples, you might want to run this script, instead of creating samplesheet.txt manually.

But it only works if you have fusion primers and paired-end merging (fwd only version coming).

Copy the script (total_creation.py) into a directory where you want to run it, which must contain the following:
1. A comma-separated file based on the sample sheet from the lab, but with only 3 columns:
Sample_name, Fusion_COI_i5_TAG_Primer, Fusion_COI_i7_TAG_Primer. Delete the rest (other columns, rows not in current project).
2. The raw .fastq files, which are named accordingly (they usually are already).

Minimal usage example: `python3 total_creation.py Ground_insects_samplesheet.csv`

Argv1 is the name of the modified samplesheet. No other arguments are required if column names are the defaults (above).
You can specify the three column names as Argv2, 3, and 4, respectively, so it will still work if they are different from the defaults.

- Must use Python3.
- Tested on Python 3.7.3, Anaconda, Inc. on Linux, Ubuntu 18.04.3 LTS.

