# robust-community-detection
Course project for CS 598 DEL, Spring 2021

This project studies _community detection_, the problem of partitioning a graph's vertices into clusters with internal connections denser than those between cluster ([Abbe 2018](doi.org/10.1561/0100000067)). 

In particular, this project studies the effectiveness of the randomized binary smoothing technique developed by [Jia et al. (2020)](doi.org/10.1145/3366423.3380029) against the "disconnect internally, connect externally (DICE)" heuristic for adversarial perturbations proposed by [Waniek et al. (2018)](doi.org/10.1038/s41562-017-0290-3). 
Experiments use the [Louvain algorithm](https://sites.google.com/site/findcommunities) for community detection; the maintained version was downloaded from [sourceforge.net/projects/louvain/](sourceforge.net/projects/louvain/) on 27 April 2021. The only dataset considered is the real-world [Email](http://snap.stanford.edu/data/email-Eu-core.html) network provided by the [Stanford Network Analysis Project](http://snap.stanford.edu/index.html). This graph has 1005 nodes, representing people in a large European research institution, and 25571 edges, representing (at least one) email communication between institution members. When edge directions and multiplicity are ignored, the resulting simple, undirected graph has 16706 edges. 

##Experimental Design

