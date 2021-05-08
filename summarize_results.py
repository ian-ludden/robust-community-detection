######################################################################
# Script for summarizing results of one trial with particular targets.
######################################################################
import sys
import utils

DEBUG = False
USAGE_STR = 'Usage: \n\tpython summarize_results.py [edges filepath] [assignment filepath] [target1] [target2] ...'
ALPHA = 0.5

if __name__ == '__main__':
    if len(sys.argv) < 4:
        raise Exception('Missing argument(s).\n{0}'.format(USAGE_STR))

    edges_fname = sys.argv[1]
    asst_fname = sys.argv[2]
    targets = [str(target) for target in sys.argv[3:]]
    
    graph = utils.load_graph_from_txt(edges_fname)
    asst = utils.load_assignment_from_txt(asst_fname)

    concealment = utils.concealment_combined(graph, asst, targets, ALPHA)
    community_labels = set(asst.values())
    communities = {i: set([node for node in graph.nodes if asst[node] == i]) for i in community_labels}
    is_detected = False
    for community in communities:
         if all(target in communities[community] for target in targets):
            is_detected = True
            break


    with open('results.out', 'a+') as f:
        f.write('\tconcealment={0:.4f},detected={1}\n'.format(concealment, int(is_detected)))
