import math
import matplotlib.pyplot as plt
f = open("outputData.txt")

horizons = [50, 200, 800, 3200, 12800, 51200, 204800]
algorithms = ["round-robin", "epsilon-greedy", "ucb", "kl-ucb", "thompson-sampling"]
epsilons = [0.002, 0.02, 0.2]

horizons_log = [math.log(i) for i in horizons]
line = f.readline()
instance1 = [[0 for j in range(len(horizons))] for i in range(len(algorithms)+2)]
instance2 = [[0 for j in range(len(horizons))] for i in range(len(algorithms)+2)]
instance3 = [[0 for j in range(len(horizons))] for i in range(len(algorithms)+2)]
total_val = 50
while line:
    line_elem = line.split(", ")
    if line_elem[0] == "../instances/i-1.txt":
        array = instance1
    elif line_elem[0] == "../instances/i-2.txt":
        array = instance2
    elif line_elem[0] == "../instances/i-3.txt":
        array = instance3
    else:
        break
    algo = algorithms.index(line_elem[1])
    horizon = horizons.index(int(line_elem[4]))
    if algo == 0:
        eps = 0
    elif algo == 1:
        eps = epsilons.index(float(line_elem[3]))
    else:
        eps = 2
    algo += eps
    array[algo][horizon] += float(line_elem[-1])
    line = f.readline()


instance1 = [[j/total_val for j in i] for i in instance1]
instance2 = [[j/total_val for j in i] for i in instance2]
instance3 = [[j/total_val for j in i] for i in instance3]

# print(instance1, instance2, instance3)
for elem in instance1:
    plt.plot(horizons_log, elem)
plt.legend(["round-robin", "epsilon-greedy(0.002)", "epsilon-greedy(0.02)", "epsilon-greedy(0.2)", "ucb", "kl-ucb", "thompson-sampling"])
plt.show()

for elem in instance2:
    plt.plot(horizons_log, elem)
plt.legend(["round-robin", "epsilon-greedy(0.002)", "epsilon-greedy(0.02)", "epsilon-greedy(0.2)", "ucb", "kl-ucb", "thompson-sampling"])
plt.show()

for elem in instance3:
    plt.plot(horizons_log, elem)
plt.legend(["round-robin", "epsilon-greedy(0.002)", "epsilon-greedy(0.02)", "epsilon-greedy(0.2)", "ucb", "kl-ucb", "thompson-sampling"])
plt.show()