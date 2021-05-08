######################################################################
# Script for sampling target set for splitting attack. 
######################################################################
import random
import sys
import utils

DEBUG = False
USAGE_STR = 'Usage: \n\tpython utils.py [edges filepath] [assignment filepath]'
BETA = 0.7
TARGET_SIZES = [2, 4, 6, 8, 10]

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
        # every ground-truth community whose size is greater than target_size. 
        for target_size in TARGET_SIZES:
            for community in communities:
                if len(communities[community]) > target_size:
                    for j in range(2):
                        targets = random.sample(communities[community], target_size)
                        f.write('{0}\n'.format(' '.join(targets)))
