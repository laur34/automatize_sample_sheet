Automating creation of samplesheet.txt
======================================

Sometimes, especially in jobs with a lot of samples, you might want to run these few scripts, instead of create samplesheet.txt manually.

But it only works if you have fusion primers and paired-end merging.

In a directory with the sample sheet from the lab, which you have modified
(1st col is Sample_name, 2nd is Fusion_COI_i5_TAG_Primer, 3rd is Fusion_COI_i7_TAG_Primer. Everything else (other columns, and rows not in project) should be deleted from it), and the appropriate raw .fastq files, 

1. First, run create_input1_and_input2_files.py, with name of 3-column sample sheet you made (must use Python3).
	example: python create_input1_and_input2_files.py samplesheet_3cols.csv
2. Next, run joining.sh.
	example: bash joining.sh

