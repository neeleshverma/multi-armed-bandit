#!/bin/sh
for instance_i in ../instances/i-1.txt ../instances/i-2.txt ../instances/i-3.txt ; do

	for horizon_i in 50  200  800  3200  12800  51200  204800 ; do

		for i in `seq 0 49`; do
			./bandit.sh --instance $instance_i --algorithm round-robin --randomSeed $i --epsilon 0.5 --horizon $horizon_i
		done

		for i in `seq 0 49`; do
			./bandit.sh --instance $instance_i --algorithm epsilon-greedy --randomSeed $i --epsilon 0.002 --horizon $horizon_i
		done

		for i in `seq 0 49`; do
			./bandit.sh --instance $instance_i --algorithm epsilon-greedy --randomSeed $i --epsilon 0.02 --horizon $horizon_i
		done

		for i in `seq 0 49`; do
			./bandit.sh --instance $instance_i --algorithm epsilon-greedy --randomSeed $i --epsilon 0.2 --horizon $horizon_i
		done

		for i in `seq 0 49`; do
			./bandit.sh --instance $instance_i --algorithm ucb --randomSeed $i --epsilon 0.5 --horizon $horizon_i
		done

		for i in `seq 0 49`; do
			./bandit.sh --instance $instance_i --algorithm kl-ucb --randomSeed $i --epsilon 0.5 --horizon $horizon_i
		done

		for i in `seq 0 49`; do
			./bandit.sh --instance $instance_i --algorithm thompson-sampling --randomSeed $i --epsilon 0.5 --horizon $horizon_i
		done

	done
done

