#!/usr/bin/bash

sort -k1,1 -t $'\t' input1.tsv > input1sorted.tsv
sort -k1,1 -t $'\t' input2.tsv > input2sorted.tsv

join -j1 input2sorted.tsv input1sorted.tsv -t $'\t' > joined.tsv
cut -f2,4,5 joined.tsv > samplesheet.txt
sed -i 's/L001_R1_001.fastq/L001_merged.fq/' samplesheet.txt
