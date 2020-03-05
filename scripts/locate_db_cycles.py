import os 
from collections import defaultdict
import networkx as nx

data_dir = '../output'

# setting a kmer size value 
k = 20 

# instantiating kmer_ids  
kmer_ids = {}
kmer_num = 0

# instantiating the digraph
db_graph = nx.DiGraph()

print('Constructing the de Bruijn graph.')
# adding di bruijn edges to graph 
seqs_fn = os.path.join(data_dir, 'SRR7225827.seqs')
with open(seqs_fn) as f: 
    for line_num, line in enumerate(f):
        line = line.strip()
    
        if (line_num + 1) % 100000 == 0:
            print('\tProcessing line number: {}'.format(line_num))
            break
        
        for i in range(len(line) - k):
            
            # get the first kmer
            first_kmer = line[i: i + k]
            
            # get the id of the first kmer 
            if first_kmer not in kmer_ids: 
                kmer_ids[first_kmer] = kmer_num
                kmer_num += 1
                first_id = kmer_ids[first_kmer]
            else:
                first_id = kmer_ids[first_kmer]

            # get the second kmer
            second_kmer = line[i + 1: i + k + 1]

            # get the id of the second kmer 
            if second_kmer not in kmer_ids: 
                kmer_ids[second_kmer] = kmer_num 
                kmer_num += 1
                second_id = kmer_ids[second_kmer]
            else:
                second_id = kmer_ids[second_kmer]

            db_graph.add_edge(first_id, second_id)

# locating all cycles in the graph 
print('Locating all cycles in the graph.')
cycles = nx.simple_cycles(db_graph)

# creating a id decoder
id_decoder = {v:k for k, v in kmer_ids.items()}

# writing all the cycles in the graph 
print('Writing all the cycles in the graph.')
cycles_fn = os.path.join(data_dir, 'SRR7225827.cycles.txt')
with open(cycles_fn, 'w') as f: 
    
    # writing all other cycles
    for i, cycle in enumerate(cycles):

        # print regular intervals 
        print('\tcycle number: {}'.format(i))

        # removing self-loops
        if len(cycle) < 2: continue 

        print('Found a longer cycle.')

        # adding the very first node of cycle to a reformatted cycle 
        re_cycle = id_decoder[cycle[0]]
        for node in cycle[1:]: 
            node_seq = id_decoder[node]
            re_cycle += node_seq[-1]

        # calculating the length of the cycle
        cycle_len = len(re_cycle)
        
        # saving the cycle with its length 
        f.write('{}\t{}\n'.format(re_cycle, cycle_len))
