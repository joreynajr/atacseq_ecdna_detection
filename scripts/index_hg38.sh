cd ../refs

# tried bowtie2 however it doesn't do split read alignment 
#bowtie2-build hg38.fa hg38.bowtie2.id

# tried STAR but it is mainly focused on RNA-seq datasets and requires a GTF
#STAR --runThreadN 1 \
#    --runMode genomeGenerate
#    --genomeDir . 
#    --genomeDir hg38.fa

bwa index hg38.fa

