from problog.engine import DefaultEngine
import trees.scoring
from trees.tilde_paper_machines_example import *

# Testing the four examples from the problog paper using the following queries:
# <- replaceable(X)
# <- not_replaceable(X)
# <- worn(X)

X = Var('X')
query1 = replaceable(X)
query2 = not_replaceable(X)
query3 = worn(X)

queries = [query1, query2, query3]

# a dictionary of sets, one for each query
results_of_queries = {}

for query in queries:
    examples_satisfying_query = trees.scoring.get_examples_satisfying_query(examples, query, background_knowledge)
    results_of_queries[query] = examples_satisfying_query

print(results_of_queries)

# entropy test
l1 = [ex2, ex3]
l2 = [ex1, ex2]
print("Entropy of 2 examples labeled 'sendback' : ", trees.scoring.entropy(l1, possible_targets), ", should be 0.0")
print("Entropy of one example labeled 'fix', another labeled 'sendback' : ", trees.scoring.entropy(l2, possible_targets), ", should be 1.0")


# information gain tests like in the TILDE paper on page 293
l_q1_l, l_q1_r = [ex1, ex2, ex3], [ex4]
l_q2_l, l_q2_r = [ex1, ex2, ex3, ex4], []
l_q3_l, l_q3_r = [ex1, ex2, ex3, ex4], []

print(trees.scoring.information_gain(examples, l_q1_l, l_q1_r, possible_targets))
print(trees.scoring.information_gain(examples, l_q2_l, l_q2_r, possible_targets))
print(trees.scoring.information_gain(examples, l_q3_l, l_q3_r, possible_targets))

