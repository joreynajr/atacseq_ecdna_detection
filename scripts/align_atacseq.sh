cd ../output

sample="SRR7225827"

# align reads to the reference genome
echo "Step 1: align reads to the reference genome"
cmd="bwa mem ../refs/hg38.fa ${sample}_1.fastq ${sample}_2.fastq > ${sample}.all_reads.sam"
#echo "Running $cmd"
#eval $cmd 

# remove mitochondrial alignments  
echo
echo "Step 2: remove mitochondrial alignments"
rm_chrM_sam=${sample}.rmChrM.sam
cmd="cat ../output/SRR7225827.all_reads.sam | \
    awk '{if(/^@/ || \$3 != 'chrM') print \$0}' > \
    $rm_chrM_sam"
echo "Running: $cmd"
eval $cmd

# sort sam file into bam file  
echo
echo "Step 3: sort alignments"
rm_chrM_bam=${bample}.rmChrM.bam
cmd="samtools view -h -S -b $rm_chrM_sam | \
    samtools sort -f - $rm_chrM_bam"
echo "Running: $cmd"
eval $cmd


# extract discordant read-pairs and split reads 
echo
echo "Step 3: extract discordant read-pairs and split reads"
discordant_fn="${sample}.samblaster.discordant_pairs.sam"
splitter_fn="${sample}.samblaster.split_reads.sam"
cmd="samblaster --input $rm_chrM_fn \
            --discordantFile $discordant_fn \
            --splitterFile $splitter_fn"
echo "Running: $cmd"
eval $cmd

