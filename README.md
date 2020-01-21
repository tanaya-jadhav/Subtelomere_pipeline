# Subtelomere_pipeline

Clusters.py: Takes 20 or less base positions, their sequences and their allele frequencies, 
picks 3 positions for clustering and generates fasta files of sequences with masked minor allele frequencies.
Matrix.py: Takes Oligotyping output and a file with sequence IDs corresponding to reads. Maps read names to Oligotyping sample IDs and separates the reads by oligotypes.
coveragescript.py: Takes a bamfile, chromosome number, start and end coordinates as input and saves a png showing coverage in current directory
