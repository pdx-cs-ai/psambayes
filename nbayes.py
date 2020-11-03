#!/usr/bin/python3

import csv, math, random, sys

# Show individual instance results.
TRACE = False

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
nsH = [nhams, nspams]

# Probability that a training message is spam.
prH = nspams / ntraining
prnotH = nhams / ntraining
prsH = [prH, prnotH]

# Per-feature probabilities of evidence given
# hypothesis. Access is nsEH[label][feature][fval].
nsEH = list()
for label in [0, 1]:
    lcounts = list()
    for f in range(nfeatures):
        counts = [0, 0]
        for inst in training:
            if inst.label == label:
                counts[inst.features[f]] += 1
        lcounts.append(counts)
    nsEH.append(lcounts)

# Return a score proportional to the Naïve Bayes
# log-likelihood that an instance has the given label.
def score_label(instance, label):
    # Compute probability of evidence given hypothesis.
    logprEH = list()
    for f in range(nfeatures):
        count = nsEH[label][f][instance.features[f]]
        logprEH.append(math.log2((count + 0.5) / (nsH[label] + 0.5)))

    return sum(logprEH) * prsH[label]

# Score test instances.
correct = 0
for inst in test:
    ss = score_label(inst, 1)
    sh = score_label(inst, 0)
    guess = int(ss > sh)
    if TRACE:
        print(inst.name, inst.label, guess)
    correct += int(inst.label == guess)

print("accuracy", correct / ntest)
