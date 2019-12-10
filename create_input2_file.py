import os, warnings

# Warning! Hyphens within core of fastq filenames will cause problems!
# Print to a file core filenames followed by respective whole filenames of fastqs.

if os.path.isfile('./input2.tsv'):
    warnings.warn('input2 file already exists! Appending to existing file. If you do not want this, delete input2.tsv and run this script again.')

f = os.popen("ls *_R1_001.fastq")
filenames = f.read()

for filename in filenames.split('\n'):
    print(filename.split('_')[0] + "\t" + filename, file=open("input2.tsv","a"))



