######################################################################
# Script for adding noise to graph for randomized smoothing.
######################################################################
import sys
import utils

DEBUG = False
USAGE_STR = 'Usage: \n\tpython add_noise_to_graph.py [edges filepath]'
BETA = 0.99

if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception('Missing argument: edges filepath.\n{0}'.format(USAGE_STR))

    edges_fname = sys.argv[1]
    asst_fname = sys.argv[2]

    graph = utils.load_graph_from_txt(edges_fname)
    noisy_graph = utils.add_edge_noise(graph, BETA)
    utils.save_graph_to_txt(noisy_graph, filename='noisy_graph.txt')
