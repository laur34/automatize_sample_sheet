Automating creation of samplesheet.txt
======================================

Sometimes, especially in jobs with a lot of samples, you might want to run these few scripts, instead of create samplesheet.txt manually.

But it only works if you have fusion primers and paired-end merging.

In a directory with the sample sheet from the lab, which you have modified according to comments in create_input1_file.py, and the appropriate raw .fastq files, 

1. First, run create_input1_file.py, with name of 3-column sample sheet you made (must use Python3).
2. Next, run create_input2_file.py (must use Python3).
3. Then, run joining.sh.

