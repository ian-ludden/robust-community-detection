######################################################################
# Script for sampling target set for splitting attack. 
######################################################################
import random
import sys
import utils

DEBUG = False
USAGE_STR = 'Usage: \n\tpython utils.py [edges filepath] [assignment filepath]'
TARGET_SIZES = [4, 6, 8]
SAMPLES_PER_COMMUNITY = 2

if __name__ == '__main__':
    if len(sys.argv) < 2: 
        raise Exception('Missing arguments: edges and assignment filepaths.\n{0}'.format(USAGE_STR))
    elif len(sys.argv) < 3:
        raise Exception('Missing argument: assignment filepath.\n{0}'.format(USAGE_STR))

    edges_fname = sys.argv[1]
    asst_fname = sys.argv[2]
    graph = utils.load_graph_from_txt(edges_fname)
    assignment = utils.load_assignment_from_txt(asst_fname)

    community_labels = set(assignment.values())
    communities = {i: set([node for node in graph.nodes if assignment[node] == i]) for i in community_labels}

    with open('targets.txt', 'w') as f:
        # For each candidate target_size, 
        # randomly sample two sets of target_size nodes from 
        # every ground-truth community whose size is 
        # greater than twice the target_size and 
        # at most four times the target_size. 
        for target_size in TARGET_SIZES:
            for community in communities:
                community_size = len(communities[community])
                if target_size <= community_size and community_size < 4 * target_size:
                    for j in range(SAMPLES_PER_COMMUNITY): # Pick samples from community
                        targets = random.sample(communities[community], target_size)
                        f.write('{0}\n'.format(' '.join(targets)))
