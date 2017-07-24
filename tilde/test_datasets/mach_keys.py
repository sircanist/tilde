from tilde.IO.parsing_settings import KeysSettingsParser
from tilde.representation.example import InternalExampleFormat
from tilde.run.run_keys import run_keys
from tilde.trees.TreeBuilder import TreeBuilderType

file_name_labeled_examples = 'D:\\KUL\\KUL MAI\\Masterproef\\data\\ACE-examples-data\\ace\\mach\\keys\\mach.kb'
file_name_settings = 'D:\\KUL\\KUL MAI\\Masterproef\\data\\ACE-examples-data\\ace\\mach\\keys\\mach.s'
file_name_background = 'D:\\KUL\\KUL MAI\\Masterproef\\data\\ACE-examples-data\\ace\\mach\\keys\mach.bg'


use_clausedb = False
debug_printing = True
use_mle = True

parsed_settings = KeysSettingsParser().parse(file_name_settings)

treebuilder_type = TreeBuilderType.DETERMINISTIC

if use_clausedb:
    internal_ex_format = InternalExampleFormat.CLAUSEDB
else:
    internal_ex_format = InternalExampleFormat.SIMPLEPROGRAM

run_keys(file_name_labeled_examples, parsed_settings, internal_ex_format, treebuilder_type,  debug_printing=debug_printing)