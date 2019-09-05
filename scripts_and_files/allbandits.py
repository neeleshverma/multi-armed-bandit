import sys
import random
import math

arguments = sys.argv[1:]
# count = len(arguments)
# print(count)

instance_file =	arguments[1]
algorithm = arguments[3]
seed = arguments[5]
epsilon = arguments[7]
horizon = int(arguments[9])

# print(seed, epsilon)
random.seed(int(seed))

arms_probabilities = []

f = open(instance_file, "r")
lines = f.readlines()
for line in lines:
	arms_probabilities.append(float(line.split("\n")[0]))

total_arms = len(arms_probabilities)
max_reward = max(arms_probabilities) * horizon

def generateReward(probability):
	reward = random.random()
	if reward < probability:
		return 1
	else:
		return 0


def roundRobin():
	REW = 0
	for i in range(horizon):
		REW += generateReward(arms_probabilities[i % total_arms])
	REG = max_reward - REW

	print(instance_file + ", " + algorithm + ", " + seed + ", " + epsilon + ", " + str(horizon) + ", " + str(REG))


def highestEmpiricalMean(empirical_means):
	indexes = []
	max_found = empirical_means[0]
	for i in range(len(empirical_means)):
		if empirical_means[i] > max_found:
			max_found = empirical_means[i]
			indexes = [i]
		elif empirical_means[i] == max_found:
			indexes.append(i)

	if len(indexes) == 1:
		return indexes[0]

	else:
		random_index = int(random.random() * len(indexes)) 
		return indexes[random_index]

def epsilonGreedy():
	REW = 0
	experimental_mean = [0.5]*total_arms
	arms_rewards = [0]*total_arms
	each_arm_pulled = [0]*total_arms

	# decider = random.random()
	for i in range(horizon):
		decider = random.random()
		if decider < float(epsilon):
			arm_index_to_pull = random.randint(0, total_arms-1)
			reward = generateReward(arms_probabilities[arm_index_to_pull])
			REW += reward
			each_arm_pulled[arm_index_to_pull] += 1
			arms_rewards[arm_index_to_pull] += reward
			# changed_mean = ((experimental_mean[arm_index_to_pull] * i) + reward) / (i+1)
			# experimental_mean = [old_mean * i / (i + 1) for old_mean in experimental_mean]
			# experimental_mean[arm_index_to_pull] = changed_mean
			experimental_mean[arm_index_to_pull] = arms_rewards[arm_index_to_pull] / each_arm_pulled[arm_index_to_pull]
		else:
			arm_index_to_pull = highestEmpiricalMean(experimental_mean)
			reward = generateReward(arms_probabilities[arm_index_to_pull])
			REW += reward
			each_arm_pulled[arm_index_to_pull] += 1
			arms_rewards[arm_index_to_pull] += reward
			# changed_mean = ((experimental_mean[arm_index_to_pull] * i) + reward) / (i+1)
			# experimental_mean = [old_mean * i / (i + 1) for old_mean in experimental_mean]
			# experimental_mean[arm_index_to_pull] = changed_mean
			experimental_mean[arm_index_to_pull] = arms_rewards[arm_index_to_pull] / each_arm_pulled[arm_index_to_pull]

	REG = max_reward - REW

	print(instance_file + ", " + algorithm + ", " + seed + ", " + epsilon + ", " + str(horizon) + ", " + str(REG))


def highestUCB(ucbs):
	indexes = []
	maximum = max(ucbs)
	for i in range(len(ucbs)):
		if ucbs[i] == maximum:
			indexes.append(i)

	return random.choice(indexes)

def UCB():
	REW = 0
	experimental_mean = [0.5]*total_arms
	ucb = [0]*total_arms
	arms_rewards = [0]*total_arms

	for i in range(total_arms):
		reward = generateReward(arms_probabilities[i])
		REW += reward
		arms_rewards[i] = reward
		experimental_mean[i] = reward 

	each_arm_pulled = [1]*total_arms

	for i in range(total_arms, horizon):
		num_term = math.sqrt(2 * math.log(i))
		for j in range(total_arms):
			ucb[j] = experimental_mean[j] + num_term / math.sqrt(each_arm_pulled[j])

		arm_index_to_pull = highestUCB(ucb)
		reward = generateReward(arms_probabilities[arm_index_to_pull])
		REW += reward
		each_arm_pulled[arm_index_to_pull] += 1
		arms_rewards[arm_index_to_pull] += reward
		experimental_mean[arm_index_to_pull] = arms_rewards[arm_index_to_pull] / each_arm_pulled[arm_index_to_pull]

	REG = max_reward - REW

	print(instance_file + ", " + algorithm + ", " + seed + ", " + epsilon + ", " + str(horizon) + ", " + str(REG))


def klDivergence(p,q):
	if p == 0 and q == 0:
		return 0
	elif p == 0 and q == 1:
		return float('inf')
	elif p == 0 and q != 0 and q != 1:
		return math.log(1/(1-q))
	elif p == 1 and q == 1:
		return 0
	elif p == 1 and q == 0:
		return float('inf')
	elif p == 1 and q != 0 and q != 1:
		return math.log(1/q)
	else:
		return p * math.log(p/q) + (1-p) * math.log((1-p)/(1-q))

def maxQval(empirical_mean, upper_limit):
	if empirical_mean == 1:
		return 1
	epsilon = 1e-7
	start = empirical_mean
	stop = 1
	while (stop - start > epsilon):
		mid_point = (start + stop) / 2
		kl_divergence = klDivergence(empirical_mean, mid_point)
		if kl_divergence < upper_limit:
			start = mid_point
		elif kl_divergence == upper_limit:
			return mid_point
		else:
			stop = mid_point

	return (start + stop)/2

def highestKLUCB(klucbs):
	indexes = []
	maximum = max(klucbs)
	for i in range(len(klucbs)):
		if klucbs[i] == maximum:
			indexes.append(i)

	return random.choice(indexes)

def klUCB():
	REW = 0
	experimental_mean = [0.5]*total_arms
	arms_rewards = [0]*total_arms
	kl_ucb = [0] * total_arms
	for i in range(total_arms):
		reward = generateReward(arms_probabilities[i])
		REW += reward
		arms_rewards[i] = reward
		experimental_mean[i] = reward
		# experimental_mean[i] = ((experimental_mean[i] * i) + reward) / (i + 1) 

	each_arm_pulled = [1]*total_arms

	for i in range(total_arms, horizon):
		upper_limit_numerator = (math.log(i) + 3 * math.log(math.log(i)))

		for j in range(total_arms):
			upper_limit = upper_limit_numerator / each_arm_pulled[j]
			kl_ucb[j] = maxQval(experimental_mean[j], upper_limit)
		
		arm_index_to_pull = highestKLUCB(kl_ucb)
		reward = generateReward(arms_probabilities[arm_index_to_pull])
		REW += reward
		each_arm_pulled[arm_index_to_pull] +=1
		arms_rewards[arm_index_to_pull] += reward
		experimental_mean[arm_index_to_pull] =  arms_rewards[arm_index_to_pull] / each_arm_pulled[arm_index_to_pull]

	REG = max_reward - REW

	print(instance_file + ", " + algorithm + ", " + seed + ", " + epsilon + ", " + str(horizon) + ", " + str(REG))


def highestBeta(beta_values):
	indexes = []
	maximum = max(beta_values)
	for i in range(len(beta_values)):
		if beta_values[i] == maximum:
			indexes.append(i)

	return random.choice(indexes)

def thompsonSampling():
	REW = 0
	successes = [0]*total_arms
	failures = [0]*total_arms
	beta_value = [0]*total_arms

	for i in range(horizon):
		for j in range(total_arms):
			beta_value[j] = random.betavariate(successes[j] + 1, failures[j] + 1)
		arm_index_to_pull = highestBeta(beta_value)
		reward = generateReward(arms_probabilities[arm_index_to_pull])
		if reward == 1:
			REW += 1
			successes[arm_index_to_pull] += 1
		else:
			failures[arm_index_to_pull] += 1

	REG = max_reward - REW

	print(instance_file + ", " + algorithm + ", " + seed + ", " + epsilon + ", " + str(horizon) + ", " + str(REG))


if algorithm == "round-robin":
	roundRobin()
elif algorithm == "epsilon-greedy":
	epsilonGreedy()
elif algorithm == "ucb":
	UCB()
elif algorithm == "kl-ucb":
	klUCB()
elif algorithm == "thompson-sampling":
	thompsonSampling()
else:
	print("Algorithm specification is wrong. Please check spelling errors")