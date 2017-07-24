from typing import List, Iterable, Sequence, Optional

from problog.logic import *

from tilde.classification.classification_helper import Label
from tilde.problog_helper.problog_helper import get_probability


def entropy_binary(list_of_bools: Sequence[bool]) -> float:
    """Calculate the entropy of a list of booleans.

        entropy([]) = 0
        entropy([True, True]) = 0
        entropy([False, False]) = 0
        entropy( [True, True, False, False]) = 1
    """
    if len(list_of_bools) == 0:
        return 0

    nb_of_positives = list_of_bools.count(True)  # type: int
    nb_of_negatives = list_of_bools.count(False)  # type: int

    if nb_of_positives == 0 or nb_of_negatives == 0:
        return 0

    return - nb_of_positives / len(list_of_bools) * math.log2(nb_of_positives / len(list_of_bools)) \
           - nb_of_negatives / len(list_of_bools) * math.log2(nb_of_negatives / len(list_of_bools))


def entropy(list_of_examples, list_of_possible_labels: Iterable[str], probabilistic:Optional[bool]=False) -> float:
    """Calculates the entropy of a list of examples. Entropy is also known as information.

    An example is an object containing a label, e.g. an instance of representation.example
    It is necessary to provide the list of all possible labels.

    :param probabilistic: 
    :param list_of_examples
            A list of examples
    :param list_of_possible_labels
            A list of possible labels
    """

    if probabilistic:
        return entropy_probabilistic(list_of_examples, list_of_possible_labels)
    else:
        if len(list_of_examples) == 0:
            return 0
        entropy_value = 0  # type: float

        nb_of_examples = len(list_of_examples)

        for label in list_of_possible_labels:
            probability_of_label = sum([get_probability(example.label) for example in list_of_examples if example.label == label])
            if probability_of_label != 0:
                entropy_value -= probability_of_label / nb_of_examples\
                                 * math.log2(probability_of_label / nb_of_examples)
        return entropy_value


def entropy_probabilistic(list_of_examples, list_of_possible_labels: Iterable[str]) -> float:
    """Calculates the entropy of a list of examples. Entropy is also known as information.

    An example is an object containing a label, e.g. an instance of representation.example
    It is necessary to provide the list of all possible labels.

    :param list_of_examples
            A list of examples
    :param list_of_possible_labels
            A list of possible labels
    """
    if len(list_of_examples) == 0:
        return 0
    entropy_value = 0  # type: float

    nb_of_examples = len(list_of_examples)  # type: int

    # TODO: assumption that an example is labeled with all label probabilities

    label_accumulators = {}

    for label in list_of_possible_labels:
        # NOTE: label is now a a set of labels
        label_accumulators[label] = 0.0

    for example in list_of_examples:
        example_labels = example.get_label_dict()
        for example_label in example_labels.keys():
            prob = example_labels[example_label]

            label_accumulators[example_label] = label_accumulators[example_label] + example_labels[example_label].value

    for label in label_accumulators.keys():
        probability_of_label = label_accumulators[label]
        if probability_of_label != 0:
            entropy_value -= probability_of_label / nb_of_examples\
                             * math.log2(probability_of_label / nb_of_examples)
    return entropy_value


def information_gain(example_list, sublist_left, sublist_right,
                     list_of_possible_labels: List[Label],
                     probabilistic:Optional[bool]=False) -> float:
    """
    Calculates the information gain of splitting a set of examples into two subsets.
    """
    if len(example_list) == 0:
        return 0

    ig = entropy(example_list, list_of_possible_labels, probabilistic)  # type: float

    ig -= len(sublist_left) / len(example_list) * entropy(sublist_left, list_of_possible_labels, probabilistic)
    ig -= len(sublist_right) / len(example_list) * entropy(sublist_right, list_of_possible_labels, probabilistic)
    return ig
