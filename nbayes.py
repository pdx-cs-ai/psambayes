#!/usr/bin/python3

import csv, random, sys

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

spams = [i for i in training if i.label == 1]
nspams = len(spams)

prH = nspams / ntraining

def product(vals):
    p = 1
    for v in vals:
        p *= v
    return p

def prob_spam(instance):
    # Compute probability of evidence.
    prE = list()
    for f in range(nfeatures):
        count = 0
        for tr in training:
            if tr.features[f] == instance.features[f]:
                count += 1
        prE.append(count / ntraining)

    # Compute probability of evidence given hypothesis.
    prEH = list()
    for f in range(nfeatures):
        count = 0
        for tr in spams:
            if tr.features[f] == instance.features[f]:
                count += 1
        prEH.append(count / nspams)

    nprEH = product(prEH)
    nprE = product(prE)
    print(nprEH, nprE)
    return  nprEH * prH / nprE

for inst in test:
    print(inst.name, inst.label, prob_spam(inst))
