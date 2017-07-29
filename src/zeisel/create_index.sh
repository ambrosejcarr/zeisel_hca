#!/usr/bin/env bash

# get index files
wget https://tools.thermofisher.com/content/sfs/manuals/ERCC92.zip
# unzip
mkdir ERCC92 && mv ERCC92.zip ERCC92/ && cd ERCC92/ && unzip ERCC92.zip && cd ../
# gzip gtf for concatenate
gzip ERCC92/ERCC92.gtf

# get mouse genome
aws s3 sync s3://hca-jamboree-data/mouse/ mouse/ --profile hca

# concatenate ercc to mouse genome
mkdir mouse_ercc
cat mouse/GRCm38.primary_assembly.genome.fasta ERCC92/ERCC92.fa > \
mouse_ercc/GRCm38.primary_assembly.genome_ercc.fasta

# concatenate ercc gtf to mouse gtf
cat mouse/gencode.vM14.annotation.gtf.gz ERCC92/ERCC92.gtf.gz > mouse_ercc/gencode.vM14.annotation_ercc.gtf.gz

# create the genome
STAR \
--runMode genomeGenerate \
--genomeDir mouse_ercc \
--genomeFastaFiles mouse_ercc/GRCm38.primary_assembly.genome_ercc.fasta \
--sjdbGTFfile mouse_ercc/gencode.vM14.annotation_ercc.gtf.gz