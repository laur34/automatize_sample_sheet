import os

# Warning! Hyphens within core of fastq filenames will cause problems!
# Print to a file core filenames followed by respective whole filenames of fastqs.

f = os.popen("ls *_R1_001.fastq")
filenames = f.read()

for filename in filenames.split('\n'):
    print(filename.split('_')[0] + "\t" + filename, file=open("input2.tsv","a"))



