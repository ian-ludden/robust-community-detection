######################################################################
# Script for running one iteration of the DICE heuristic on a graph.
# Overwrites the edges file that was given. 
######################################################################
import sys
import utils

DEBUG = False
USAGE_STR = 'Usage: \n\tpython run_dice.py [edges filepath] [target1] [target2] ...'

if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception('Missing argument: edges filepath.\n{0}'.format(USAGE_STR))

    edges_fname = sys.argv[1]
    targets = [str(target) for target in sys.argv[2:]]
    
    graph = utils.load_graph_from_txt(edges_fname)
    graph_after_dice = utils.execute_dice(graph, targets)
    utils.save_graph_to_txt(graph_after_dice, filename=edges_fname)
