#!/bin/sh
# Script for CS 598 DEL final project experiments, 
# exploring the effectiveness of the randomized smoothing 
# strategy developed by Jia et al. (2020) in thwarting 
# the DICE heuristic attack against community detection 
# presented in Waniek et al. (2018).  

LOG_FILE="results.out"

# Select target (a.k.a. victim) sets for splitting attacks
py pick_targets.py data/email.txt data/email_labels.txt
dos2unix targets.txt

# Iterate over T trials
T=5 # Number of trials
N=10 # Number of samples for randomized smoothing
echo "Running experiments with" $T "trials and" $N "samples for randomized smoothing."
for trial in $(seq 1 $T)
do
    echo "Trial $trial"
    echo "Trial $trial" >> "$LOG_FILE"

    NUM_TARGETS=$(wc -l < "targets.txt")
    # echo "There are" $NUM_TARGETS "lines in targets.txt."
    targets_index=0
    while read target_list
    do
        echo $target_list
        echo $target_list >> "$LOG_FILE"

        # Create fresh copy of the Email-EU core graph in this folder. 
        cp data/email.txt graph.txt

        # Run |target_list| steps of: 
        # (1) DICE, then 
        # (2) N iterations of randomized smoothing. 
        step_count=0
        for target in $target_list
        do
            ((step_count=step_count+1))
            echo "Step" "$step_count" >> "$LOG_FILE"
            echo "    Concealment,Detected" >> "$LOG_FILE"
            py run_dice.py graph.txt $target_list

            for iteration in $(seq 1 $N)
            do
                py add_noise_to_graph.py graph.txt noisy_graph.txt
                convert_louvain.exe -i noisy_graph.txt -o noisy_graph.bin
                louvain.exe noisy_graph.bin -l -1 -v -q id_qual > noisy_graph.tree
                hierarchy_out=$(hierarchy.exe noisy_graph.tree)
                IFS=' ' read -ra hierarchy_out_words <<< "$hierarchy_out"
                max_level=$(expr "${hierarchy_out_words[3]}" - 1)
                echo "max level:" $max_level
                echo ""
                hierarchy.exe noisy_graph.tree -l $max_level > assignments.txt
                py summarize_results.py noisy_graph.txt assignments.txt $target_list
            done
        done
        ((targets_index=targets_index+1))
    done < "targets.txt"

done
