from typing import Iterable, Set

from problog.engine import DefaultEngine

from tilde.classification.classification_helper import Label
from tilde.representation.example import SimpleProgramExample, ClauseDBExample, InternalExampleFormat, \
    InternalExampleFormatException, Example


class LabelCollector:
    def __init__(self, predicate_to_query, index_of_label_var, background_knowledge=None):
        self.engine = DefaultEngine()
        self.engine.unknown = 1
        if background_knowledge is not None:
            self.db = self.engine.prepare(background_knowledge)
        else:
            self.db = None
        self.predicate_to_query = predicate_to_query
        self.labels = set()  # type: Set[Label]
        self.index_of_label_var = index_of_label_var

    def get_labels(self) -> Set[Label]:
        return self.labels

    def extract_labels(self, examples: Iterable[Example]):
        raise NotImplementedError('Abstract method')


class SimpleProgramLabelCollector(LabelCollector):
    def extract_label(self, example: SimpleProgramExample):
        if self.db is not None:
            db_example = self.db.extend()
            for statement in example:
                db_example += statement
        else:
            db_example = self.engine.prepare(example)

        list_of_answers = self.engine.query(db_example, self.predicate_to_query)
        if len(list_of_answers) is 0:
            raise Exception("Querying the predicate", self.predicate_to_query, "on the example gives no results")
        for answer in list_of_answers:
            label = answer[self.index_of_label_var]
            self.labels.add(label)
            example.label = label

    def extract_labels(self, examples: Iterable[SimpleProgramExample]):
        for example in examples:
            self.extract_label(example)


class ClauseDBLabelCollector(LabelCollector):
    def extract_labels(self, example_dbs: Iterable[ClauseDBExample]):
        for db_example in example_dbs:  # type: ClauseDBExample
            list_of_answers = self.engine.query(db_example, self.predicate_to_query)
            if len(list_of_answers) is 0:
                raise Exception("Querying the predicate", self.predicate_to_query, "on the example gives no results")
            for answer in list_of_answers:
                label = answer[self.index_of_label_var]
                self.labels.add(label)
                db_example.label = label


class LabelCollectorMapper:

    @staticmethod
    def get_label_collector(internal_ex_format: InternalExampleFormat, predicate_to_query, index_of_label_var, background_knowledge=None):
        if internal_ex_format is internal_ex_format.CLAUSEDB:
            return ClauseDBLabelCollector(predicate_to_query, index_of_label_var, background_knowledge)
        elif internal_ex_format is InternalExampleFormat.SIMPLEPROGRAM:
            return SimpleProgramLabelCollector(predicate_to_query, index_of_label_var, background_knowledge)
        else:
            raise InternalExampleFormatException("Only the internal formats SimpleProgram and ClauseDB are supported, "
                                                 "got: " + str(internal_ex_format))