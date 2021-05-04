######################################################################
# Utility functions for graph I/O and basic graph operations. 
######################################################################
import networkx as nx
import numpy as np
import os
from pprint import pprint
import random
import sys

def load_graph_from_txt(edges_fname):
    """
    Given a text file with a "<src> <dest>" edge pair on each line, 
    constructs and returns the corresponding 
    simple, undirected graph as a networkx Graph object. 
    """
    graph = nx.Graph()

    with open(edges_fname, 'r') as f:
        for line in f:
            src, dest = line.strip('\n').split(' ')
            graph.add_edge(src, dest)

    print('{0} nodes, {1} edges'.format(graph.number_of_nodes(), graph.number_of_edges()))
    return graph


def load_assignment_from_txt(asst_fname):
    """
    Given a text file with a "<node> <part>" pair on each line, 
    constructs a dictionary mapping nodes to parts. 
    """
    assignment = {}

    with open(asst_fname, 'r') as f:
        for line in f:
            node, part = line.strip('\n').split(' ')
            assignment[node] = int(part)

    return assignment


def concealment_1(graph, assignment, targets):
    """
    TODO: implement
    Given a graph, an assignment into partitions/clusters, 
    and a set of target vertices (a.k.a. evaders), 
    computes the first concealment measure, mu prime, 
    defined by Waniek et al. (2018). 

    The assignment is given as a dictionary of 
    <node label>:<part> pairs, where <node label> is a string and 
    <part> is an integer. 
    """
    community_labels = set(assignment.values())
    
    target_assignments = [assignment[target] for target in targets]
    target_communities, target_community_freqs = np.unique(target_assignments, return_counts=True)

    denom_1 = max(len(community_labels) - 1, 1)
    denom_2 = max(target_community_freqs)

    return (len(target_communities) - 1) / (denom_1 * denom_2)


def concealment_2(graph, assignment, targets):
    """
    Given a graph, an assignment into partitions/clusters, 
    and a set of target vertices (a.k.a. evaders), 
    computes the second concealment measure, mu double prime, 
    defined by Waniek et al. (2018). 
    """
    community_labels = set(assignment.values())
    communities = {i: set([node for node in graph.nodes if assignment[node] == i]) for i in community_labels}
    
    target_assignments = [assignment[target] for target in targets]
    target_communities, target_community_freqs = np.unique(target_assignments, return_counts=True)
    target_communities = list(target_communities)

    numerators = []
    for community in community_labels:
        comm_size = len(communities[community])
        if community in target_communities:
            target_comm_index = target_communities.index(community)
            numerators.append(comm_size - target_community_freqs[target_comm_index])
        else:
            numerators.append(0) # Exclude communities containing none of the targets

    denominator = 1. * max(len(graph.nodes) - len(targets), 1)
    return np.sum([numerator / denominator for numerator in numerators])


def concealment_combined(graph, assignment, targets, alpha):
    """
    Returns a convex combination of concealment_1 and concealment_2: 
        alpha * concealment_1 + (1 - alpha) * concealment_2
    """
    return alpha * concealment_1(graph, assignment, targets) \
        + (1 - alpha) * concealment_2(graph, assignment, targets)


if __name__ == '__main__':
    USAGE_STR = 'Usage: \n\tpython utils.py [edges filepath] [assignment filepath]'
    ALPHA = 0.5

    if len(sys.argv) < 2: 
        raise Exception('Missing arguments: edges and assignment filepaths.\n{0}'.format(USAGE_STR))
    elif len(sys.argv) < 3:
        raise Exception('Missing argument: assignment filepath.\n{0}'.format(USAGE_STR))

    edges_fname = sys.argv[1]
    asst_fname = sys.argv[2]
    graph = load_graph_from_txt(edges_fname)
    assignment = load_assignment_from_txt(asst_fname)

    # Test concealment

    ## Handle sample from Waniek et al. Figure 4 differently
    if edges_fname == 'data\\fig4.txt':
        num_targets = 4
        targets = ['4', '5', '6', '7']
    else:
        num_targets = 4
        targets = random.sample(graph.nodes, k=num_targets)

    c1 = concealment_1(graph, assignment, targets)
    c2 = concealment_2(graph, assignment, targets)
    c = concealment_combined(graph, assignment, targets, alpha=ALPHA)

    print('Targets: {0}'.format(targets))
    print('Concealment 1: {0:.3f}\nConcealment 2: {1:.3f}\nCombined: {2:.3f}'.format(c1, c2, c))

    print()
