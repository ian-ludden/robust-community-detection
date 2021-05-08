######################################################################
# Script for running one iteration of the DICE heuristic on a graph.
######################################################################
import sys
import utils

DEBUG = False
USAGE_STR = 'Usage: \n\tpython run_dice.py [edges filepath] [target1] [target2] ...'
BETA = 0.9

if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception('Missing argument: edges filepath.\n{0}'.format(USAGE_STR))

    edges_fname = sys.argv[1]
    targets = [str(target) for target in sys.argv[2:]]
    
    graph = utils.load_graph_from_txt(edges_fname)

    noisy_graph = utils.add_edge_noise(graph, BETA)
    utils.save_graph_to_txt(noisy_graph, filename='noisy_graph.txt')
