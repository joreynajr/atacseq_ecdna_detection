data_dir='../output'
cat "$data_dir/SRR7225827_1.fastq" | awk '{if(NR % 4 == 2) print $0}' > "$data_dir/SRR7225827.seqs"
cat "$data_dir/SRR7225827_2.fastq" | awk '{if(NR % 4 == 2) print $0}' >> "$data_dir/SRR7225827.seqs"
