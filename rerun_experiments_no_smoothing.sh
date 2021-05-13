#!/bin/sh
# Script for repeating the experiments of 
# run_experiments.sh, but without randomized smoothing, 
# to use as a control. 

LOG_FILE="results.out"

# Run Louvain method to find initial communities
convert_louvain.exe -i data/email.txt -o data/email.bin
louvain.exe data/email.bin -l -1 -v -q id_qual > data/email.tree
hierarchy_out=$(hierarchy.exe data/email.tree)
IFS=' ' read -ra hierarchy_out_words <<< "$hierarchy_out"
max_level=$(expr "${hierarchy_out_words[3]}" - 1)
echo "max level:" $max_level
echo ""
hierarchy.exe data/email.tree -l $max_level > data/initial_louvain_communities.txt

# Select target (a.k.a. victim) sets for splitting attacks
py pick_targets.py data/email.txt data/initial_louvain_communities.txt
dos2unix targets.txt

# Iterate over T trials
T=5 # Number of trials
echo "Running experiments with" $T "trials"
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

        # TODO: consider running Louvain with 0 executions of DICE 
        # to determine initial concealment. 
        # 
        # It could be that DICE is having little/no observed effect because 
        # we are picking targets from ground-truth communities instead of 
        # from initial Louvain communities. If Louvain is already confused, 
        # then DICE isn't really needed/helpful. 

        # Run |target_list| steps of DICE
        step_count=0
        for target in $target_list
        do
            ((step_count=step_count+1))
            echo "Step" "$step_count" >> "$LOG_FILE"
            echo "    Concealment,Detected" >> "$LOG_FILE"
            py run_dice.py graph.txt $target_list

            convert_louvain.exe -i graph.txt -o graph.bin
            louvain.exe graph.bin -l -1 -v -q id_qual > graph.tree
            hierarchy_out=$(hierarchy.exe graph.tree)
            IFS=' ' read -ra hierarchy_out_words <<< "$hierarchy_out"
            max_level=$(expr "${hierarchy_out_words[3]}" - 1)
            echo "max level:" $max_level
            echo ""
            hierarchy.exe graph.tree -l $max_level > assignments.txt
            py summarize_results.py graph.txt assignments.txt $target_list
        done
        ((targets_index=targets_index+1))
    done < "targets.txt"

done
