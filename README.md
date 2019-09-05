# multi-armed-bandit
Algorithms for solving multi armed bandit problem

Implementation of following 5 algorithms for solving multi-armed bandit problem:-
1. **Round robin**
2. **Epsilon-greedy**
3. **UCB**
4. **KL-UCB**
5. **Thompson sampling**

3 bandit instances files are given in instance folder. They contain the probabilties of bandit arms. 

3 graphs are plotted for 3 bandit instances. They show the performance of 5 algorithms ( + 3 epsilon-greedy algorithms with different epsilons)

To run the code, run the script wrapper.sh. Otherwise run bandit.sh as follows :-

** ./bandit.sh --instance instance_file_location --algorithm round-robin --randomSeed 10 --epsilon 0.5 --horizon 10 **

**@** Here algorithm can be any one of 5 - {round-robin, epsilon-greedy, ucb, kl-ucb, thompson-sampling}. 

**@** Random seed can be any integer value for the seed of random function in python 

**@** epsilon in {0,1}  

**@** Horizon -> Any positive integer value
