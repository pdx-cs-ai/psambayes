#!/usr/bin/python3

import csv, math, random, sys

# Class of instances.
class Instance(object):
    def __init__(self, row):
        self.name = row[0]
        self.label = int(row[1])
        self.features = [int(f) for f in row[2:]]

# Read instances.
with open(sys.argv[1], "r") as f:
    reader = csv.reader(f)
    instances = [Instance(row) for row in reader]

# Number of instances.
ninstances = len(instances)

# Number of features per instance. XXX Should be same for
# all instances.
nfeatures = len(instances[0].features)

random.shuffle(instances)

# Split into training and test set.
split = ninstances // 2
training = instances[split:]
ntraining = len(training)
test = instances[:split]
ntest = len(test)

# Split training into hams and spams.
spams = [i for i in training if i.label == 1]
nspams = len(spams)
hams = [i for i in training if i.label == 0]
nhams = len(hams)

# Probability that a training message is spam.
prH = nspams / ntraining

# Return a score proportional to the Naïve Bayes
# log-likelihood that an instance is spam.
def score_spam(instance):
    # Compute probability of evidence given hypothesis.
    logprEH = list()
    for f in range(nfeatures):
        count = 0
        for tr in spams:
            if tr.features[f] == instance.features[f]:
                count += 1
        logprEH.append(math.log2((count + 0.5) / (nspams + 0.5)))

    return sum(logprEH) * prH

# Return a score proportional to the Naïve Bayes
# log-likelihood that an instance is ham.
# XXX Heavy copy-paste from above.
def score_ham(instance):
    # Compute probability of evidence given hypothesis.
    logprEH = list()
    for f in range(nfeatures):
        count = 0
        for tr in hams:
            if tr.features[f] == instance.features[f]:
                count += 1
        logprEH.append(math.log2((count + 0.5) / (nhams + 0.5)))

    return sum(logprEH) * prH

# Score test instances.
correct = 0
for inst in test:
    ss = score_spam(inst)
    sh = score_ham(inst)
    guess = int(ss > sh)
    print(inst.name, inst.label, guess)
    correct += int(inst.label == guess)

print("accuracy", correct / ntest)
